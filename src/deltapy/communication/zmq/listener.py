'''
Created on Sep 16, 2014

@author: Abi.Mohammadi
'''

import json
import traceback
import multiprocessing
from threading import Thread

import zmq

from deltapy.communication.listener import Listener
from deltapy.core import DeltaException, DeltaObject
from deltapy.communication.listener import Dispatcher
from deltapy.communication.marshal import JSONCustomDecoder,\
    JSONCustomEncoder
import deltapy.logging.services as logging


def make_error_result(type_converter, exception, **kwargs):
    '''
    Raises a structured exception based on the given message and keyword arguments

    @param str message: message

    @keyword str code: code
    @keyword dict data: data
    @keyword str traceback: traceback

    @rtype: None
    @return nothing

    @raise: Exception
    '''

    # Converting the exception message to the targeted output format
    message = type_converter.to_external(str(exception))

    # Creating a new exception instance with the given message
    ex = dict(code=None, message=message, data={})

    if isinstance(exception , DeltaException):
        ex['code'] = type_converter.to_external(exception.get_code())
        ex['data'] = type_converter.to_external(exception.get_data())
        ex['traceback'] = type_converter.to_external(exception.get_traceback())

    # Trying to get the true traceback from the exception object.
    # This attribute has been set by RequestProcessor before.
    if ex.get('traceback') is None:
        if hasattr(exception, 'traceback'):
            ex['traceback'] = type_converter.to_external(getattr(exception, 'traceback'))
        else:
            ex['traceback'] = type_converter.to_external(traceback.format_exc(exception))

    return dict(__EXCEPTION__=ex)

class ZmqDispatcher(Thread):
    '''
    Zmq distpatcher.
    '''
    
    def __init__(self, listener, context, dealer_url):
        super(ZmqDispatcher, self).__init__()
        self._listener = listener
        self._dealer_url = dealer_url
        self._keep_going = True
        self._context = context
    
    def _get_client_ip_(self, **options):
        '''
        Detects and returns client IP address.
        '''

        return '127.0.0.1'

    def login_ex(self, user_name, password, options):
        return self._listener.login_ex(self._get_client_ip_(),
                                       user_name,
                                       password,
                                       **options)

    def logout(self, ticket, user_name):
        return self._listener.logout(self._get_client_ip_(),
                                     ticket,
                                     user_name)

    def execute_ex(self, request, options):
        request['ip'] = self._get_client_ip_()
        if options is None:
            options = {}
        return self._listener.execute_ex(request, **options)
    
    def run(self):
        commands = dict(login=self.login_ex,
                        logout=self.logout,
                        execute=self.execute_ex)
        
        self._socket = self._context.socket(zmq.REP)
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.connect(self._dealer_url)
        while self._keep_going:
            message = self._socket.recv()
            try:
                what_to_run = json.loads(message, cls=JSONCustomDecoder)
                command = what_to_run['command']
                data = what_to_run['data']
                response = commands.get(command)(**data)
                buf = json.dumps(response, cls=JSONCustomEncoder)
                self._socket.send(buf)
            except Exception as e:
                message = make_error_result(self._listener.get_type_convertor(), e)
                self._socket.send(json.dumps(message, cls=JSONCustomEncoder))
        
    def shutdown(self):
        self._keep_going = False
        self._socket.close()
        

class ZmqListener(Listener):
    '''
    ZMQ listener.
    '''
    
    logger = logging.get_logger(name = 'ZMQ')
    
    def __init__(self, communicator, name, params, client_request_class=None):
        '''
        '''
        
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)
        
        # Configuring Zmq
        workers_count = params.get('workers')
        if workers_count is not None:
            workers_count = int(workers_count)
        else:
            workers_count = 16
        
        if not params.has_key('service_name'): 
            params['service_name'] = self.get_name()
            
        router_url = 'tcp://{0}:{1}'.format(params.get('host'), params.get('port'))
        dealer_url = 'inproc://workers'
        
        # Creating zmq context    
        io_threads = multiprocessing.cpu_count() - 1
        if io_threads < 2:
            io_threads = 2;
        self._context = zmq.Context(io_threads)
        
        # Creating router socket
        self._router = self._context.socket(zmq.ROUTER)
        self._router.setsockopt(zmq.LINGER, 0)
        self._router.bind(router_url)
        
        # Creating dealer socket
        self._dealer = self._context.socket(zmq.DEALER)
        self._dealer.setsockopt(zmq.LINGER, 0)
        self._dealer.bind(dealer_url)
        
        self._dispatchers = []
        for index in xrange(workers_count):
            dispatcher = ZmqDispatcher(self, self._context, dealer_url)
            self._dispatchers.append(dispatcher)
            
    def login(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        
        return Listener.login(self, ip, user_name, password, **options)
   
    def login_ex(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        
        try:
            return Listener.login_ex(self,ip, user_name, password, **options)
        except Exception, error:
            return make_error_result(self.get_type_convertor(), error)

    def execute_ex(self, request, **options):
        '''
        Executes the command by the given command key.
        
        @param request: client request
        
        @return: Response
        '''
    
        try:
            result = Listener.execute_ex(self,
                                         request,
                                         **options)
            return result
        except Exception, error:
            return make_error_result(self.get_type_convertor(), error)
        
    def start(self):
        '''
        Starts the listener.
        '''
        
        for dispatcher in self._dispatchers:
            dispatcher.start()
        zmq.device(zmq.QUEUE, self._router, self._dealer)

    def stop(self, force):
        '''
        Stops the listener.
        '''

        for dispatcher in self._dispatchers:
            dispatcher.shutdown()
            
        self._dealer.close()
        self._router.close()
        self._context.term()
