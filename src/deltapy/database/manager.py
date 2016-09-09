'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

from threading import Lock

from deltapy.core import DeltaObject, DeltaException
from deltapy.database.connection_pool import ConnectionPool

class DatabaseManagerException(DeltaException):
    '''
    Contains database manager errors.
    '''
    pass 

class DatabasePoolNotFoundException(DatabaseManagerException):
    '''
    '''

class DatabaseManager(DeltaObject):
    '''
    Provides management on database pools.
    '''
    
    def __init__(self):
        self._lock = Lock()
        self.__pools = {}
        
    def add_pool(self,
                 connection_pool):
        if connection_pool.get_name() in self.__pools:
            raise DatabaseManagerException('Connection pool[%s] already exsits.' % connection_pool)
        self.__pools[connection_pool.get_name()] = connection_pool
    
    def open(self, pool_name = None):
        _pool_name = ConnectionPool.DEFAULT
        if pool_name is not None:
            _pool_name = pool_name
        pool = self.__pools.get(_pool_name)
        if pool is None:
            message = 'Database pool [{pool_name}] not found.'
            raise DatabasePoolNotFoundException(message.format(pool_name = _pool_name))
        return pool.acquire()
    
    def close(self, connection):
        self.__pools[connection.pool_name].release(connection)
    
    def get_pools(self):
        return self.__pools.values()
    
    def reset_pools(self):
        self.__pools = {}
            