'''
Created on Oct 11, 2015

@author: Hamed
'''

from deltapy.communication.factory import CommunicationFactory
from deltapy.communication.ice.listener import IceListener
from deltapy.communication.ice.proxy import IceProxy
from deltapy.communication.ice.ice_client_request import IceRawRequest


class IceFactory(CommunicationFactory):

    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        '''
        Create ice proxy by given ticket and other configs.

        @param str ticket: ticket
        @param str user_name: user name

        @keyword str service_name: service name
        @keyword str protocol: network protocol
        @note protocol:
            'tcp'
            'ssl'
        @keyword str Ice.Plugin.IceSSL: Ice plugin
        @keyword str IceSSL.Ciphers: Ice ssl ciphers
        @keyword str IceSSL.VerifyPeer: Ice ssl verify peer

        @rtype: object
        @return: instance of IceProxy
        '''
        host = kwargs.pop('host', None)
        port = int(kwargs.pop('port', None))
        return IceProxy(ticket, user_name, host, port, **kwargs)

    def create_listener(self, communicator, name, params):
        listener = IceListener(communicator, name, params,
                               client_request_class=IceRawRequest)

        return listener
