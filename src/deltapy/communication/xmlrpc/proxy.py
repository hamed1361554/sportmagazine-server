'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import xmlrpclib
from deltapy.communication.proxy import Proxy

class XmlrpcProxy(Proxy):
    def __init__(self, ticket, user_name, host, port, service_name):
        Proxy.__init__(self, ticket, user_name)
        url = 'http://%s:%d' % (host, int(port))
        self._service_name = service_name
        self._server_proxy = xmlrpclib.Server(url)

    def execute_by_user(self, ticket, user_name, command_key , *args, **kargs):
        method_name = "%s.execute" % self._service_name
        method = getattr(self._server_proxy, method_name)
        return method(ticket, 
                      user_name, 
                      command_key, 
                      *args, 
                      **kargs)
