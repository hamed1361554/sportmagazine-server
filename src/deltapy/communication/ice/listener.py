'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
import time

import sys
import traceback

import Ice
import DeltaIce

from deltapy.core import DeltaException
from deltapy.communication.listener import Listener
from deltapy.communication.listener import Dispatcher
from deltapy.communication.ice import utils
from deltapy.locals import get_app
import deltapy.logging.services as logging
from deltapy.security.authentication.authenticator import AuthenticationException


class IceDispatcher(DeltaIce.IIceDispatcher, Dispatcher):

    logger = logging.get_logger(name='communicator')

    def __init__(self, listener):
        Dispatcher.__init__(self, listener)

    def _get_client_ip_(self, **options):
        current = options.get('current')
        if current is not None:
            ip_port = current.con.toString().split('remote address = ')[1]
            ip_address = ip_port.split(':')[0]
            return utils.object_to_dobject(ip_address)
    
    def login(self, userName, password, options, current = None):
        try:
            start = time.time()

            login_result = \
                self._listener.login(self._get_client_ip_(current=current),
                                     userName,
                                     password,
                                     **options)

            end = time.time()
            ticket = login_result.value['ticket'].value
            time_span = end - start
            IceDispatcher.logger.info("Ice [{0}] login [{1}]".format(ticket,
                                                                     time_span))

            return login_result
        except DeltaException as error:
            exception = DeltaIce.AuthenticationException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if error.get_traceback() is not None:
                exception.traceback = utils.str_to_external(error.get_traceback())
            else:
                exception.traceback = utils.str_to_external(traceback.format_exc())

            raise exception

        except Exception as error:
            exception = DeltaIce.GenericException()
            exception.message = utils.str_to_external(str(error))
            
            # Getting the true trace back from the error itself.
            if hasattr(error, 'traceback'):
                exception.traceback = getattr(error, 'traceback')
            else:
                exception.traceback = traceback.format_exc()
            raise exception

    def loginEx(self, userName, password, options, current=None):
        try:
            start = time.time()

            login_result = \
                self._listener.login_ex(self._get_client_ip_(current=current),
                                        userName,
                                        password,
                                        **options)

            end = time.time()
            ticket = login_result.value['ticket'].value
            time_span = end - start
            IceDispatcher.logger.info("Ice [{0}] login [{1}]".format(ticket,
                                                                     time_span))

            return login_result

        except DeltaException as error:
            exception = DeltaIce.AuthenticationException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if error.get_traceback() is not None:
                exception.traceback = utils.str_to_external(error.get_traceback())
            else:
                exception.traceback = utils.str_to_external(traceback.format_exc())

            raise exception

        except Exception as error:
            exception = DeltaIce.GenericException()
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if hasattr(error, 'traceback'):
                exception.traceback = getattr(error, 'traceback')
            else:
                exception.traceback = traceback.format_exc()
            raise exception
        
    def logout(self, ticket, userName, current=None):
        try:
            start = time.time()

            logout_result = \
                self._listener.logout(self._get_client_ip_(current=current),
                                      ticket,
                                      userName)

            end = time.time()
            time_span = end - start
            IceDispatcher.logger.info("Ice [{0}] logout [{1}]".format(ticket.value,
                                                                      time_span))

            return logout_result

        except Exception as error:
            exception = DeltaIce.GenericException()
            exception.message = str(error)

            # Getting the true trace back from the error itself.
            if hasattr(error, 'traceback'):
                exception.traceback = getattr(error, 'traceback')
            else:
                exception.traceback = traceback.format_exc()
            raise exception
    
    def execute(self, ticket, userName, commandKey, args, kwargs, current=None):
        try:
            execute_result = \
                self._listener.execute(self._get_client_ip_(current=current),
                                       ticket,
                                       userName,
                                       commandKey,
                                       *args,
                                       **kwargs)

            return execute_result

        except DeltaException as error:
            exception = DeltaIce.GenericException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if error.get_traceback() is not None:
                exception.traceback = utils.str_to_external(error.get_traceback())
            else:
                exception.traceback = utils.str_to_external(traceback.format_exc())

            raise exception

        except Exception as error:
            exception = DeltaIce.GenericException()
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if hasattr(error, 'traceback'):
                exception.traceback = getattr(error, 'traceback')
            else:
                exception.traceback = traceback.format_exc()
            raise exception

    def executeEx(self, request, current=None):
        try:
            start = time.time()

            request['ip'] = self._get_client_ip_(current=current)
            execute_result = \
                self._listener.execute_ex(request)

            end = time.time()
            request_id = execute_result.value['request_id'].value
            time_span = end - start
            IceDispatcher.logger.info("Ice [{0}] executed [{1}]".format(request_id,
                                                                        time_span))

            return execute_result

        except DeltaException, error:
            exception = DeltaIce.GenericException()
            exception.code = error.get_code()
            exception.data = utils.object_to_dobject(error.get_data())
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if error.get_traceback() is not None:
                exception.traceback = utils.str_to_external(error.get_traceback())
            else:
                exception.traceback = utils.str_to_external(traceback.format_exc())

            raise exception

        except Exception, error:
            exception = DeltaIce.GenericException()
            exception.message = utils.str_to_external(str(error))

            # Getting the true trace back from the error itself.
            if hasattr(error, 'traceback'):
                exception.traceback = getattr(error, 'traceback')
            else:
                exception.traceback = traceback.format_exc()
            raise exception

class IceListener(Listener):

    def __init__(self, communicator, name, params, client_request_class=None):
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)

        if not params.has_key('service_name'): 
            params['service_name'] = self.get_name()

        host = params.get('host')
        port = int(params.get('port'))
        protocol = params.get('protocol')
        if protocol is None:
            protocol = 'tcp'

        ice_url = "%s -h %s -p %d" % (protocol, host, port)

        properties = Ice.createProperties()

        for property_name, property_value in params.iteritems():
            #Passing configs to Ice as properties. Ice will pick its
            #own configs and ignore others.
            properties.setProperty(property_name, property_value)
        
        data = Ice.InitializationData()
        data.properties = properties
        
        self._proxy = Ice.initialize(sys.argv, data)
        self._adapter = self._proxy.createObjectAdapterWithEndpoints(get_app().get_name(), 
                                                                     ice_url)
        
        self.add_service(IceDispatcher(self), name = params['service_name'])
        
    def add_service(self, service, **kwargs):
        '''
        Add a service to listener.
        
        @param service: service object
        '''
        
        name = kwargs.get('name', None)
        
        self._adapter.add(service, self._proxy.stringToIdentity(name))
        self._adapter.activate()

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

        logout_result = \
            self._communicator.logout(self, logout_request)

        return logout_result

    def execute(self, ip, ticket, user_name, command_key, *args, **kargs):
        '''
        Executes the given command.
        
        @param ip: client ip
        @param ticket: user ticket
        @param user_name: user name
        @param command_key: command key
        
        @return: object
        
        @note: This method is existed for backward compatibility.
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

        return result.value['result']

    def start(self):
        self._proxy.waitForShutdown() 

    def stop(self, force):
        self._proxy.destroy()

