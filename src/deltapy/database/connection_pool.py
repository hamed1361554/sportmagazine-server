'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.utils.object_pool import ObjectPool
from deltapy.utils.encryption import decrypt
from deltapy.event_system.decorators import delta_event

class ConnectionPool(ObjectPool):
    
    DEFAULT = 'default'

    def __init__(self, 
                 name, 
                 connection_string, 
                 min, 
                 max, 
                 growup, 
                 **options):
        ObjectPool.__init__(self, name, min, max, growup, **options)

        encrypted_password = options.get('encrypted_password')
        if encrypted_password is not None:
            connection_string = connection_string.replace('*', decrypt(eval(encrypted_password)))
            
        self._connection_string = connection_string
            
    def _create_object_(self):
        '''
        Creates a new object
        
        @return: object
        '''
        
        return self._create_connection_()

    def _destroy_object_(self, object):
        '''
        Destroys object.
        
        @param object: object instance
        '''
        
        return self._close_connection_(object)
        
    def _create_connection_(self):
        raise NotImplementedError()

    def _close_connection_(self, connection):
        raise NotImplementedError()

    def acquire(self):
        '''
        Acquires a connection from pool.
        
        @return: object
        '''
        return super(ConnectionPool, self).acquire()
        
    def release(self, object):
        '''
        Releases connection.
        
        @param object: object instance
        '''
        return super(ConnectionPool, self).release(object)
