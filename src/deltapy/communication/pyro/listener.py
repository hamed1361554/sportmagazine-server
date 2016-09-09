'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import traceback

import Pyro.core
import Pyro.naming
import Pyro.constants
from Pyro.protocol import DefaultConnValidator

import deltapy.logging.services as logging
from deltapy.communication.listener import Listener
from deltapy.core import DeltaException, DeltaObject
from deltapy.communication.listener import Dispatcher
from deltapy.communication.pyro.type_convertor import PyroTypeConvertor

class PyroExceptionManager(DeltaObject):
    '''
    Manages exception instantiation and type conversion
    '''

    def __init__(self):
        '''
        Initializes the class instance
        '''

        self.type_converter = PyroTypeConvertor()

    def raise_exception(self, exception, **kwargs):
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
        message = self.type_converter.to_external(exception.message)

        # Creating a new exception instance with the given message
        ex = Exception(message)

        code = None
        data = {}
        traceback = None

        # Formatting and setting optional exception code, if it is provided
        if hasattr(exception, 'code'):
            code = self.type_converter.to_external(exception.code)
        ex.code = code

        # Formatting and setting optional exception data, if it is provided
        if hasattr(exception, 'data'):
            data = self.type_converter.to_external(exception.data)
            ex.data = data

        # Formatting and setting optional exception traceback, if it is provided
        if hasattr(exception, 'traceback'):
            traceback_data = self.type_converter.to_external(exception.traceback)
            ex.traceback = traceback_data

        raise ex

    def to_internal(self, exception, **kwargs):
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
        message = self.type_converter.to_internal(exception.message)

        # Creating a new exception instance with the given message
        ex = Exception(message)

        code = None
        data = {}
        traceback = None

        # Formatting and setting optional exception code, if it is provided
        if hasattr(exception, 'code'):
            code = self.type_converter.to_internal(exception.code)
        elif hasattr(exception, 'get_code'):
            code = self.type_converter.to_internal(exception.get_code())
        ex.code = code

        # Formatting and setting optional exception data, if it is provided
        if hasattr(exception, 'data'):
            data = self.type_converter.to_internal(exception.data)
            ex.data = data
        elif hasattr(exception, 'get_data'):
            data = self.type_converter.to_internal(exception.get_data())
            ex.data = data

        # Formatting and setting optional exception traceback, if it is provided
        if hasattr(exception, 'traceback'):
            traceback_data = self.type_converter.to_internal(exception.traceback)
            ex.traceback = traceback_data

        raise ex


class ConnectionValidator(DefaultConnValidator):
    '''
    Connection validator for PYRO.
    '''
    
    def acceptIdentification(self, 
                             daemon, 
                             connection, 
                             token, 
                             challenge):
        '''
        ???
        
        @param daemon: daemon instance
        @param connection: connection
        @param token: token
        @param challenge: challenge
        '''
        return 1,0
        #return (0,Pyro.constants.DENIED_SECURITY)

class PyroDispatcher(Pyro.core.ObjBase, Dispatcher):
    '''
    Pyro distpatcher.
    '''
    def __init__(self, listener):
        Pyro.core.ObjBase.__init__(self)
        Dispatcher.__init__(self, listener)

    def _get_client_ip_(self, **options):
        '''
        Detects and returns client IP address.
        '''
        return self.getLocalStorage().caller.addr[0]

class PyroListener(Listener):
    '''
    Pyro listener.
    '''
    
    logger = logging.get_logger(name = 'PYRO')
    
    def __init__(self, communicator, name, params, client_request_class=None):
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)

        if not params.has_key('service_name'): 
            params['service_name'] = self.get_name() 

        Pyro.config.PYRO_MULTITHREADED = 1
        Pyro.core.initServer()
        self._daemon = Pyro.core.Daemon(host = self.host, port = self.port)
        #self.__daemon.setNewConnectionValidator(ConnectionValidator())
        self.add_service(PyroDispatcher(self), name = params['service_name'])
        self._exception_manager = PyroExceptionManager()

    def login(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        try:
            return Listener.login(self, ip, user_name, password, **options)
        except DeltaException, error:
            # As login method calls login_ex method of the communicator, the raised
            # exception is already formatted when it reaches this method; hence, no
            # reformatting is needed.
            raise error
        except Exception, error:
            raise error
   
    def login_ex(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        try:
            return Listener.login_ex(self,ip, user_name, password, **options)
        except DeltaException, error:
            self._exception_manager.raise_exception(error)
        except Exception, error:
            self._exception_manager.raise_exception(error)

    def execute(self, 
                ip_address, 
                ticket, 
                user_name, 
                command_key, 
                *args, 
                **kargs):
        '''
        Executes the command by the given command key.
        
        @param ip_address: client IP address
        @param ticket: security ticket
        @param user_name: user name
        @param command_key: command key
        '''

        try:
            result = Listener.execute(self,
                                      ip_address,
                                      ticket,
                                      user_name,
                                      command_key,
                                      *args,
                                      **kargs)
            return result

        except DeltaException, error:
            message = str(error)
            ex = Exception(message)
            ex.code = error.get_code()
            ex.data = error.get_data()
            ex.traceback = traceback.format_exc()
            PyroListener.logger.exception(ex)
            self._exception_manager.raise_exception(ex)
        except Exception, error:
            message = str(error)
            ex = Exception(message)
            ex.traceback = traceback.format_exc()
            PyroListener.logger.exception(ex)
            self._exception_manager.raise_exception(ex)

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

        except DeltaException, error:
            message = str(error)
            ex = Exception(message)
            ex.code = error.get_code()
            ex.data = error.get_data()
            ex.traceback = traceback.format_exc()
            PyroListener.logger.exception(ex)
            self._exception_manager.raise_exception(ex)
        except Exception, error:
            message = str(error)
            ex = Exception(message)
            ex.traceback = traceback.format_exc()
            PyroListener.logger.exception(ex)
            self._exception_manager.raise_exception(ex)
        
    def add_service(self, service, **kwargs):
        '''
        Add a service to listener.
        
        @param service: service object
        '''

        name = kwargs.get('name', None)
        self._daemon.connect(service, name)

    def start(self):
        '''
        Starts the listener.
        '''
        
        self._daemon.requestLoop()

    def stop(self, force):
        '''
        Stops the listener.
        '''
        
        self._daemon.shutdown()
