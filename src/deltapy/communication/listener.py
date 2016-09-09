'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

from deltapy.core import DeltaException, DynamicObject
from deltapy.core import DeltaObject
from deltapy.request_processor.request import RawRequest

class ListenerException(DeltaException):
    pass

class Dispatcher(DeltaObject):
    def __init__(self, listener):
        DeltaObject.__init__(self)
        self._listener = listener

    def _get_client_ip_(self, **options):
        return 'unknown'

    def login(self, user_name, password, **kwargs):
        return self._listener.login(self._get_client_ip_(**kwargs),
                                    user_name, 
                                    password,
                                    **kwargs)
        
    def login_ex(self, user_name, password, **kwargs):
        return self._listener.login_ex(self._get_client_ip_(**kwargs),
                                       user_name, 
                                       password,
                                       **kwargs)

    def logout(self, ticket, user_name, **kwargs):
        return self._listener.logout(self._get_client_ip_(**kwargs),
                                     ticket, 
                                     user_name,
                                     **kwargs)
    
    def execute(self, ticket, user_name, command_key, *args, **kwargs):
        result = self._listener.execute(self._get_client_ip_(**kwargs),
                                       ticket, 
                                       user_name, 
                                       command_key, 
                                       *args, 
                                       **kwargs)
        return result
        
    def execute_ex(self, request, **options):
        request['ip'] = self._get_client_ip_()
        response = self._listener.execute_ex(request, **options)
        return response

class Listener(DeltaObject):

    def __init__(self, communicator, name, params, client_request_class=None):
        '''
        @param instance communicator: Instance of the communicator that
            this listener should work with.
        @param str name: Name of this listener.
        @param dict params: Configuration parameters for this listener.
        @keyword instance client_request_class: The class that should carry
            request around. Default is ClientRequest.
        '''
        DeltaObject.__init__(self)
        
        self.host = params.get('host')
        self.port = int(params.get('port'))
        self.__name = name
        self.__params = params
        self._communicator = communicator
        self.__enable = True
        self._client_request_class = client_request_class

        if self._client_request_class is None:
            self._client_request_class = RawRequest
        
    def get_name(self):
        '''
        Returns the listener name.
        
        @return: str
        '''
        return self.__name

    def add_service(self, service, **kwargs):
        '''
        Add a service to listener.
        
        @param service: service object
        '''
        raise NotImplementedError()

    def start(self):
        '''
        Starts this listener.
        '''
        raise NotImplementedError()

    def stop(self):
        '''
        Stops this listener.
        '''
        raise NotImplementedError()

    def enable(self, flag):
        '''
        Enables or disables the listener.
        
        @param flag: True or False
        '''
        self.__enable = flag
        
    def is_enable(self):
        '''
        Returns True if the listener is enabled.
        
        @return: boolean
        '''
        return self.__enable

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
        
        return result['ticket']

    def login_ex(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        '''
        login_request = self._client_request_class(DynamicObject(ip=ip,
                                                                 user_name=user_name,
                                                                 password=password,
                                                                 options=options))
        
        return self._communicator.login(self, login_request)

    def logout(self, ip, ticket, user_name):
        '''
        Log outs the user.
         
        @param ip: client ip
        @param ticket: user ticket
        @param user_name: user name
        '''
        logout_request = self._client_request_class(DynamicObject(ip=ip,
                                                                  ticket=ticket,
                                                                  user_name=user_name))

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
        request = self._client_request_class(DynamicObject(request_id=None,
                                                           transaction_id=None,
                                                           request_date=None,
                                                           ip=ip,
                                                           ticket=ticket,
                                                           user_name=user_name,
                                                           command_key=command_key,
                                                           command_args=args,
                                                           command_kwargs=kargs,
                                                           timeout=None,
                                                           context=None))

        response = self._communicator.execute(self, request)

        return response['result']

    def execute_ex(self, request, **options):
        '''
        Executes the given request.
        
        @param request: client request
        
        @return: object
        '''
        # Sending request to the communicator.
        # Note that we created an instance from the specified `Client Request'
        # class to pass this data around.
        response =  self._communicator.execute(self,
                                               self._client_request_class(request),
                                               **options)
        
        return response

    def get_params(self):
        '''
        Returns the listener parameters.
        
        @return: dict
        '''
        
        return self.__params
