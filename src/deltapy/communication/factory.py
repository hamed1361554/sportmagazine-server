'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaException, DeltaObject

class CommunicationFactory(DeltaObject):
    def create_proxy(self, user_name, password, **kwargs):
        proxy = self.create_proxy_by_ticket(None, user_name, **kwargs)
        proxy.open(user_name, password, **kwargs)
        return proxy
    
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        raise NotImplementedError()
    
    def create_listener(self, communicator, name, params):
        raise NotImplementedError()
        
