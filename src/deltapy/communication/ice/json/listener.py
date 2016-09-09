'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import sys

import Ice
import DeltaIce

from deltapy.communication.listener import Listener
from deltapy.communication.ice.json.dispatcher import IceJsonDispatcher
from deltapy.locals import get_app

class IceJsonListener(Listener):
    
    #logger = logging.get_logger(name = 'IceDispatcher')
    
    def __init__(self, communicator, name, params, client_request_class=None):
        Listener.__init__(self, communicator, name, params, client_request_class=client_request_class)

        if not params.has_key('service_name'): 
            params['service_name'] = self.get_name()

        host = params.get('host')
        port = int(params.get('port'))
        protocol = params.get('protocol')
        if protocol is None:
            protocol = 'tcp'

        ice_url = "%s -h %s -p %d" % (protocol, host, port)

        properties = Ice.createProperties()

        for property_name, property_value in params.iteritems():
            #Passing configs to Ice as properties. Ice will pick its
            #own configs and ignore others.
            properties.setProperty(property_name, property_value)
        
        data = Ice.InitializationData()
        data.properties = properties
        
        self._proxy = Ice.initialize(sys.argv, data)
        self._adapter = self._proxy.createObjectAdapterWithEndpoints(get_app().get_name(), 
                                                                            ice_url)
        
        self.add_service(IceJsonDispatcher(self), name = params['service_name'])
        
    def add_service(self, service, **kwargs):
        '''
        Add a service to listener.
        
        @param service: service object
        '''
        
        name = kwargs.get('name', None)
        
        self._adapter.add(service, self._proxy.stringToIdentity(name))
        self._adapter.activate()

    def start(self):
        self._proxy.waitForShutdown() 

    def stop(self, force):
        self._proxy.destroy()

