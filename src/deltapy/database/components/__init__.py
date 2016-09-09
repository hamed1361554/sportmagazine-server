'''
Created on Dec 19, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from threading import Lock

import deltapy.config.services as config
import deltapy.application.services as application

from deltapy.database.manager import DatabaseManager, DatabaseManagerException
from deltapy.storm.connection_pool import StoreConnectionPool
from deltapy.application.decorators import register
from deltapy.locals import APP_DATABASE

@register(APP_DATABASE)
class DatabaseManagerComponent(DatabaseManager):
    '''
    '''
    
    def __init__(self):
        DatabaseManager.__init__(self)
        
        self.make_defined_pools()

    def open(self, pool_name = None):
        if len(self.get_pools()) == 0:
            try:
                self._lock.acquire()
                if len(self.get_pools()) == 0:
                    self.make_defined_pools()
            finally:
                self._lock.release()
        return DatabaseManager.open(self, pool_name)

    def make_defined_pools(self):
        '''
        Makes connection pools by database configuration.
        '''
        
        # Getting a configuration store on database settings
        config_store = config.get_app_config_store('database')
        
        # Getting default pool name
        default_pool_name = config_store.get('global', 'default', None)
        if default_pool_name is None:
            raise DatabaseManagerException('Default connection pool is not determined.')

        # Getting all sections in database settings
        sections = config_store.get_sections()
        
        for name in sections:
            if name != 'global':
                data = config_store.get_section_data(name)

                connection_string = data.get('connection', None)
                if not connection_string:
                    raise DatabaseManagerException('Connection pool[%s] has not connection string.' % name)
                
                connection_string = application.get_real_path(connection_string)
                
                pool_name = name
                if name == default_pool_name:
                    pool_name = StoreConnectionPool.DEFAULT
                    
                min_connections = int(data.get('min', 0))
                max_connections = int(data.get('max', 0))
                growup = int(data.get('growup', 0))
                encrypted_password = data.get('encrypted_password', None)
                life_time = data.get('life_time', None)
                
                pool = StoreConnectionPool(pool_name, 
                                           connection_string, 
                                           min_connections, 
                                           max_connections, 
                                           growup,
                                           encrypted_password = encrypted_password,
                                           life_time = life_time)
                
                self.add_pool(pool)
    
        