'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.pymp.listener import PympListener
from deltapy.communication.pymp.proxy import PympProxy

class PympFactory(CommunicationFactory):
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        return PympProxy(ticket, user_name)
    
    def create_proxy(self, user_name, password, **kwargs):
        pass
    
    def create_listener(self, communicator, name, params):
        return PympListener(communicator, name, params)