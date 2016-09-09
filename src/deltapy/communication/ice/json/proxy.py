'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import sys
import Ice

from DeltaIce import IIceDispatcherPrx

from deltapy.communication.proxy import Proxy, ProxyPingException
import deltapy.communication.ice.utils as ice_utils
import deltapy.communication.ice.json.utils as json_utils


class IceJsonProxy(Proxy):
    def __init__(self, ticket, user_name, host, port, **configs):
        Proxy.__init__(self, ticket, user_name)


        service_name = configs.pop('service_name', None)
        protocol = configs.pop('protocol', None)

        if service_name is None:
            service_name = 'ice'

        if protocol is None:
            protocol = 'tcp'

        ice_url = '%s:%s -h %s -p %d' % (service_name, protocol, host, port)

        properties = Ice.createProperties()

        for property_name, property_value, in configs.iteritems():
            properties.setProperty(property_name, property_value)

        data = Ice.InitializationData()
        data.properties = properties

        self._communicator = Ice.initialize(sys.argv, data)
        self._server_proxy = IIceDispatcherPrx.checkedCast(self._communicator.stringToProxy(ice_url))

    def open(self, user_name, password, **options):
        '''
        
        @param user_name:
        @param password:
        '''
        
        ticket = self._server_proxy.login(user_name, password, options)
        self.ticket = ticket
        self.user_name = user_name
        
    def execute_by_user(self, ticket, user_name, command_key , *args, **kargs):
        t_args = None

        if args:
            t_args = ice_utils.list_to_dlist(list(args))
        t_kwargs = ice_utils.dict_to_ddict(kargs)
        command_key = ice_utils.object_to_dobject(command_key)
        user_name = ice_utils.object_to_dobject(user_name)
        ticket = ice_utils.object_to_dobject(ticket)

        result = self._server_proxy.execute(ticket, 
                                            user_name, 
                                            command_key, 
                                            t_args, 
                                            t_kwargs)        
        return json_utils.dobject_to_object(result)
    
    def close(self):
        self._server_proxy.logout(self.ticket, self.user_name)

    def ping(self):
        '''
        Probes the remote dispatcher.
        '''
        
        try:
            self._server_proxy.ice_ping()
        except Exception, e:
            raise ProxyPingException(str(e))
        
