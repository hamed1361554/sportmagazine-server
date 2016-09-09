'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import time

from deltapy.database.manager import ConnectionPool 
from storm.locals import create_database, Store
from deltapy.storm.transactional_store import TransactionalStore 

class StoreConnectionPool(ConnectionPool):

    def __init__(self, 
                 name, 
                 connection_string, 
                 min, 
                 max, 
                 growup,
                 **options):
        
        ConnectionPool.__init__(self, name, connection_string, min, max, growup, **options)
        self.__life_time = options.get('life_time')
        if self.__life_time is None or self.__life_time < 0:
            # Default is 8 hours.
            self.__life_time = 8 * 60 * 60
            
        self.__database = create_database(self._connection_string)
        
    def _is_object_alive_(self, object):            
        '''
        Return True if object is alive.
        
        @param object: object object
        @return: bool
        '''
        
        return self._is_connection_alive_(object)

    def _is_connection_alive_(self, connection):            
        '''
        Return True if connection is alive.
        
        @param connection: connection object
        @return: bool
        '''
        # Checking life time of the connection.
        if self.__life_time > 0 and time.time() - connection.creation_date > self.__life_time:
            return False
        
        # Checking if connection still alive.
        try:
            connection.execute('select 1 from dual')
        except Exception:
            return False

        return True

    def _create_connection_(self):
        store = TransactionalStore(self.__database)
        store.pool_name = self.get_name()
        store.creation_date = time.time()
        return store

    def _close_connection_(self, connection):
        try:
            connection.close()
        except Exception:
            pass

    def _acquire_(self):
        '''
        Acquires an object from pool.
        
        @return: object
        '''
        return ConnectionPool._acquire_(self)
 
    def __str__(self):
        return "[%s-%s]" % (self.get_name(), self._connection_string)
