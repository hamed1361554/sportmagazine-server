'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.listener import Listener
from deltapy.communication.listener import Dispatcher
from SimpleXMLRPCServer import SimpleXMLRPCServer
from DocXMLRPCServer import DocXMLRPCServer
import deltapy.logging.services as logging

class XmlrpcDispatcher(Dispatcher):
    def __init__(self, listener):
        Dispatcher.__init__(self, listener)

    def _get_client_ip_(self, **options):
        return '127.0.0.1'
    
class XmlrpcListener(Listener):
    
    logger = logging.get_logger(name = 'xmlrpc')
    
    def __init__(self, communicator, name, params, client_request_class=None):
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)
        
        if not params.has_key('service_name'): 
            params['service_name'] = self.get_name()
        
        host = params.get('host')
        port = int(params.get('port'))
            
        self._server = DocXMLRPCServer(addr = (host, port), 
                                       allow_none = 1, 
                                       logRequests = 0)

        self.add_service(XmlrpcDispatcher(self), name = params['service_name'])

    def __get_instance_methods__(self, instance, prefix = None):
        methods = {}
        for o in dir(instance):
            if not o.startswith('_'):
                method = getattr(instance, o)
                if method.__class__.__name__ == 'instancemethod':
                    if prefix:
                        methods["%s.%s" % (prefix, o)] = method
                    else:
                        methods[o] = method
        return methods
        
    def add_service(self, service, **kwargs):
        '''
        Add a service to listener.
        
        @param service: service object
        '''

        name = kwargs.get('name', None)
        methods = self.__get_instance_methods__(service, name)
        for method_name, method in methods.items():
            self._server.register_function(method, method_name)
            
    def start(self):
        self._server.serve_forever()

    def stop(self, force):
        try:
            self._server.shutdown()
        except Exception, error:
            XmlrpcListener.logger.warning(error)
        
    
