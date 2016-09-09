'''
Created on Oct 11, 2015

@author: Hamed
'''

import traceback

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from deltapy.communication.thrift.services.DeltaThriftDispatcher import Processor

from deltapy.core import DeltaException
from deltapy.communication.listener import Listener
from deltapy.communication.listener import Dispatcher

from deltapy.communication.thrift.services.ttypes import *


class ThriftDispatcher(Dispatcher):
    '''
    Thrift Dispatcher
    '''

    def __init__(self, listener):
        Dispatcher.__init__(self, listener)

    def _get_client_ip_(self, **options):
        return utils.object_to_dobject('192.168.22.88')
        current = options.get('current')
        if current is not None:
            ip_port = current.con.toString().split('remote address = ')[1]
            ip_address = ip_port.split(':')[0]
            return utils.object_to_dobject(ip_address)
    
    def login(self, userName, password, options, current = None):
        try:
            return self._listener.login(self._get_client_ip_(current = current), 
                                        userName, 
                                        password,
                                        **options)
        except DeltaException as error:
            exception = AuthenticationException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception as error:
            exception = GenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = traceback.format_exc()
            raise exception

    def loginEx(self, userName, password, options, current = None):
        try:
            return self._listener.login_ex(self._get_client_ip_(current = current), 
                                           userName, 
                                           password,
                                           **options)
        except DeltaException as error:
            exception = AuthenticationException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception as error:
            exception = GenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = traceback.format_exc()
            raise exception
        
    def logout(self, ticket, userName, current = None):
        try:
            return self._listener.logout(self._get_client_ip_(current = current), 
                                         ticket, 
                                         userName)
        except Exception as error:
            exception = GenericException()
            exception.message = str(error)
            exception.traceback = traceback.format_exc()
            raise exception
    
    def execute(self, ticket, userName, commandKey, args, kwargs, current = None):
        try:
            return self._listener.execute(self._get_client_ip_(current = current),
                                          ticket, 
                                          userName, 
                                          commandKey,
                                          *args,
                                          **kwargs)
        except DeltaException as error:
            exception = GenericException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception as error:
            exception = GenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = traceback.format_exc()
            raise exception

    def executeEx(self, request, current = None):
        try:
            request['ip'] = self._get_client_ip_(current=current)
            return self._listener.execute_ex(request)
        except DeltaException, error:
            exception = GenericException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception, error:
            exception = GenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = traceback.format_exc()
            raise exception

class ThriftListener(Listener):
    '''
    Thrift Listener
    '''
    
    def __init__(self, communicator, name, params, client_request_class=None):
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)

        if 'service_name' not in params:
            params['service_name'] = self.get_name()

        host = params.get('host')
        port = int(params.get('port'))

        self._handler = ThriftDispatcher(self)
        self._processor = Processor(self._handler)
        self._transport = TSocket.TServerSocket(host=host, port=port)
        self._transport_factory = TTransport.TBufferedTransportFactory()
        self._protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

        self._server = TServer.TThreadedServer(self._processor,
                                               self._transport,
                                               self._transport_factory,
                                               self._protocol_factory)

    def login(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        
        @note: This method is existed for backward compability.
            `login_ex' should be used instead.
        '''
        result = self.login_ex(ip, user_name, password, **options)
        
        return result.value['ticket']

    def login_ex(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        request_dict = DeltaIce.DictObject()
        request_dict.value = {'ip': ip,
                              'user_name': user_name,
                              'password': password,
                              'options': options}
        
        login_request = self._client_request_class(request_dict)
        
        return self._communicator.login(self, login_request)

    def logout(self, ip, ticket, user_name):
        '''
        Log outs the user.
         
        @param ip: client ip
        @param ticket: user ticket
        @param user_name: user name
        '''
        request_dict = DeltaIce.DictObject()
        request_dict.value = {'ip': ip,
                              'ticket': ticket,
                              'user_name': user_name}

        logout_request = self._client_request_class(request_dict)

        return self._communicator.logout(self, logout_request)

    def execute(self, ip, ticket, user_name, command_key, *args, **kargs):
        '''
        Executes the given command.
        
        @param ip: client ip
        @param ticket: user ticket
        @param user_name: user name
        @param command_key: command key
        
        @return: object
        
        @note: This method is existed for backward compability.
            `execute_ex' should be used instead.
        '''
        request_dict = DeltaIce.DictObject()
        request_dict.value = {'request_id': None,
                              'transaction_id': None,
                              'request_date': None,
                              'ip': ip,
                              'ticket': ticket,
                              'user_name': user_name,
                              'command_key': command_key,
                              'command_args': args,
                              'command_kwargs': kargs,
                              'timeout': None,
                              'context': None}
        request = self._client_request_class(request_dict)

        result = self._communicator.execute(self, request)
        
        return result.value['response']

    def start(self):
        self._server.serve()

    def stop(self, force):
        pass

