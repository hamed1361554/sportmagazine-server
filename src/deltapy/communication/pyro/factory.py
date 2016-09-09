'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.pyro.listener import PyroListener
from deltapy.communication.pyro.proxy import PyroProxy
from deltapy.communication.pyro.client_request import PyroRawRequest

class PyroFactory(CommunicationFactory):
    
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        host = kwargs.get('host', None)
        port = int(kwargs.get('port', None))
        service_name = kwargs.get('service_name', None)        
        return PyroProxy(ticket, user_name, host, port, service_name)
    
    def create_listener(self, communicator, name, params):
        listener = PyroListener(communicator, name, params, client_request_class=PyroRawRequest)
        return listener
