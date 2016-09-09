'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.ice.json.listener import IceJsonListener
from deltapy.communication.ice.json.proxy import IceJsonProxy
from deltapy.communication.ice.json.client_request import IceJsonRawRequest


class IceJsonFactory(CommunicationFactory):

    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        host = kwargs.get('host', None)
        port = int(kwargs.get('port', None))
        return IceJsonProxy(ticket, user_name, host, port, **kwargs)

    def create_listener(self, communicator, name, params):
        listener = IceJsonListener(communicator, name, params, client_request_class=IceJsonRawRequest)
        return listener
