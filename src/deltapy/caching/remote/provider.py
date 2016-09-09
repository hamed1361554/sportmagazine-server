'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import cPickle
import socket 

from deltapy.core import DeltaObject, DynamicObject, DeltaException
from deltapy.caching.remote.connection import RemoteCacheConnection
from deltapy.utils.decorators import singleton
import deltapy.config.services as config_services
import deltapy.application.services as app_services

MAX_DATA_SIZE = 1024 * 1024

class RemoteCacheProviderException(DeltaException):
    '''
    '''

@singleton
class RemoteCacheProvider(DeltaObject):
    '''
    Remote Cache provider.
    '''
    def __init__(self):
        DeltaObject.__init__(self)
        self._connection_data = None
        self.setup(app_services.get_full_name())
    
    def _create_cache_(self, sock, ip, name, data):
        request = ('create', name, data)
        request= cPickle.dumps(request)
        sock.send(request)
        response = sock.recv(MAX_DATA_SIZE)
        port, auth_key = cPickle.loads(response)
        if port == 0:
            raise RemoteCacheProviderException("Could'nt create cache[{name}]".format(name = name))
        return DynamicObject(ip = ip, 
                             cache_port = port, 
                             auth_key = auth_key)

    def setup(self, name, **params):
        '''
        Setups all providers.
        @param name: initialization name.
        @param **params:
            ip: cache server IP
            port: cache server main port
            auth_key: authentication key 
            cache_port: cache service port
        '''

        config_store = config_services.get_app_config_store('caching')
        enable = eval(config_store.get('remote_cache', 'enable', 'False'))
        if not config_store.has_section('remote_cache') or not enable:
            return None
        
        config_params = config_store.get_section_data('remote_cache')
        config_params.update(params)

        # Reading configurations
        ip = config_params.get('ip', None)
        port = config_params.get('port', 0)
        if port is not None:
            port = int(config_params.get('port', 0))
        data = {}
        data['name'] = name
        data['ip'] = ip
        data['port'] = port
        data['auth_key'] = config_params.get('auth_key', None)
        data['cache_port'] = config_params.get('cache_port', 0)
        if data['cache_port']:
            data['cache_port'] = int(data['cache_port'])

        # Creating socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
                
        connection_data = self._create_cache_(sock, ip, name, data)
        connection_data['port'] = port
        connection_data['ip'] = ip
        self._connection_data = connection_data
        
        return connection_data

       
    def get_connection(self):
        '''
        Returns a new connection to remote cache server.
        '''
        if self._connection_data == None:
            raise RemoteCacheProviderException('Cache provider not connected. a remote cache should be setuped.')
        return RemoteCacheConnection(self._connection_data.ip,
                                     self._connection_data.cache_port,
                                     self._connection_data.auth_key)
        

