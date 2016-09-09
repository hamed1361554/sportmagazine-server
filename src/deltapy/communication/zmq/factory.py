'''
Created on Sep 17, 2014

@author: Abi.Mohammadi
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.zmq.listener import ZmqListener
from deltapy.communication.zmq.proxy import ZmqProxy
from deltapy.communication.zmq.client_request import ZmqRawRequest


class ZmqFactory(CommunicationFactory):
    '''
    ZMQ factory class
    '''
    
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        '''
        Creates a proxy.
        
        @return: ZMQ proxy
        '''
        host = kwargs.get('host', None)
        port = int(kwargs.get('port', None))
        service_name = kwargs.get('service_name', None)        
        return ZmqProxy(ticket, user_name, host, port, service_name)
    
    def create_listener(self, communicator, name, params):
        '''
        Creates listener.
        
        @return: ZMQ listener
        '''
        
        listener = ZmqListener(communicator, name, params, client_request_class=ZmqRawRequest)
        return listener
