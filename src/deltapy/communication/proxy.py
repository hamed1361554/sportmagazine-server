'''
Created on Sep 27, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaException, DeltaObject

class ProxyException(DeltaException):
    '''
    '''

class ProxyPingException(ProxyException):
    '''
    '''

class Proxy(DeltaObject):
    '''
    '''

    def __init__(self, ticket, user_name):
        self.ticket = ticket
        self.user_name = user_name
        
    def open(self, user_name, password, **options):
        '''
        
        @param user_name:
        @param password:
        '''
        
        raise NotImplementedError()
    
    def execute(self, command_key , *args, **kargs):
        return self.execute_by_user(self.ticket, self.user_name, command_key, *args, **kargs)
    
    def execute_ex(self, request, **options):
        raise NotImplementedError()

    def execute_by_user(self, ticket, user_name, command_key , *args, **kargs):
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError()
    
    def ping(self):
        pass
    
    