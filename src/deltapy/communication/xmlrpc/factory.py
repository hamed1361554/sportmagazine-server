'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.xmlrpc.listener import XmlrpcListener
from deltapy.communication.xmlrpc.proxy import XmlrpcProxy
from deltapy.communication.xmlrpc.client_request import XmlrpcRawRequest


class XmlrpcFactory(CommunicationFactory):
    
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        host = kwargs.get('host', None)
        port = int(kwargs.get('port', None))
        service_name = kwargs.get('service_name', None)        
        return XmlrpcProxy(ticket, user_name, host, port, service_name)
    
    def create_proxy(self, user_name, password, **kwargs):
        pass
    
    def create_listener(self, communicator, name, params):
        listener = XmlrpcListener(communicator, name, params,
                                  client_request_class=XmlrpcRawRequest)
        return listener
