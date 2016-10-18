'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
import time
import sys

import Ice
import DeltaIce

from deltapy.communication.listener import Listener
from deltapy.communication.ice.json.dispatcher import IceJsonDispatcher
from deltapy.locals import get_app
import deltapy.logging.services as logging

class IceJsonListener(Listener):
    
    #logger = logging.get_logger(name = 'IceDispatcher')

    communicator_logger = logging.get_logger(name='communicator')
    
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
        
    def login(self, ip, user_name, password, **options):
        '''
        Logins in application.
        
        @param ip: client IP address
        @param user_name: user name
        @param password: user password
        
        @note: This method is existed for backward compability.
            `login_ex' should be used instead.
        '''
        start = time.time()
        login_result = \
            super(IceJsonListener, self).login(ip, user_name, password, **options)

        end = time.time()
        time_span = end - start
        IceJsonListener.communicator_logger.info("Ice-Json [{0}] login [{1}]".format(login_result,
                                                                                     time_span))

        return login_result

    def logout(self, ip, ticket, user_name):
        '''
        Log outs the user.

        @param ip: client ip
        @param ticket: user ticket
        @param user_name: user name
        '''
        start = time.time()
        logout_result = \
            super(IceJsonListener, self).logout(ip, ticket, user_name)

        end = time.time()
        time_span = end - start
        IceJsonListener.communicator_logger.info("Ice-Json [{0}] logout [{1}]".format(ticket,
                                                                                      time_span))
        return logout_result

    def execute_ex(self, request, **options):
        '''
        Executes the given request.

        @param request: client request

        @return: object
        '''
        start = time.time()

        execute_result = \
            super(IceJsonListener, self).execute_ex(request, **options)

        end = time.time()
        request_id = execute_result["request_id"]
        time_span = end - start
        IceJsonListener.communicator_logger.info("Ice-Json [{0}] executed [{1}]".format(request_id,
                                                                                        time_span))

        return execute_result