'''
Created on Oct 22, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException
from deltapy.utils.uniqueid import get_uuid
import time

class CacheException(DeltaException):
    '''
    A class for handling cache exceptions.
    '''
    pass

class CacheItem:
    '''
    Contains cached items information.
    '''
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.creation_time = time.time()
        self.last_reset_time = time.time()
        self.hit_count = 0
        self.miss_count = 0   
        self.expired = False
        
    def __str__(self):
        return "CacheItem[%s:%s]" % (self.key, self.value)
 
    def __repr__(self):
        return str(self)

class CacheBase(DeltaObject):
    '''
    
    '''
    
    def __init__(self, cache_name, **options):
        DeltaObject.__init__(self)
        self._set_name_(cache_name)
        self.__cache_id = get_uuid()
        self._creation_time = time.time()
        self._last_reset_time = time.time()
        self._lifetime = None
        self._scavenger = options.get('scavenger', None)
        if self._scavenger is not None:
            self._scavenger.initialize(self)
        self._size = int(options.get('size', 1024))
    
    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''      
        raise NotImplementedError()
    
    def __len__(self):
        return self.get_len()
    
    def get_id(self):
        '''
        Returns cache id.
        
        @return: object
        '''
        
        return self.__cache_id
    
    def set_size(self, size):
        '''
        Sets cache size.
        
        @param size: cache new size 
        '''
        
        raise NotImplementedError()
        
        
    def get_size(self):
        '''
        Returns cache size.
        
        @return: int
        '''
        
        return self._size

    def set_scavenger(self, scavenger):
        '''
        Sets cache scavenger.
        
        @param scavenger: scavenger 
        '''
        
        self._scavenger = scavenger
        if self._scavenger is not None:
            self._scavenger.initialize(self)
        
    def get_scavenger(self):
        '''
        Returns cache scavenger.
        
        @return: IScavenger
        '''
        
        return self._scavenger

    def reset_item(self, key):
        '''
        Resets cache item.
        '''
        
        raise NotImplementedError()

    def clear(self):
        '''
        Removes all cache items.
        '''

        raise NotImplementedError()
    
    def pop(self, key):
        '''
        Pops specified item.
        
        @param key: item key
        
        @return: object
        '''
        
        value = self[key]
        self.remove(key)
        return value
        
    def remove(self, key):
        '''
        Removes specified item from cache. 
        
        @param key: item key
        '''
        
        raise NotImplementedError()
    
    def reset(self):
        '''
        Resets the cache.
        '''
        
        raise NotImplementedError()
        
    def set(self, key, value):
        '''
        '''
        
        raise NotImplementedError()
        
    def get(self, key, default = None):
        '''
        '''

        raise NotImplementedError()
    
    def has_key(self, key):
        '''
        '''
        
        raise NotImplementedError()
    
    def get_items(self):
        '''
        '''
        
        raise NotImplementedError()
    
    def set_items(self):
        '''
        '''

        raise NotImplementedError()
        
    def __hash__(self):
        '''
        '''
        
        return hash(self.get_id())
        
    def __setitem__(self, key, value):
        '''
        '''
        
        return self.set(key, value)
        
    def __getitem__(self, key):
        '''
        '''
        result = self.get(key, KeyError)
        if result is KeyError:
            raise KeyError('Item with key[%s] not found.' % key)
        return result
    
    def __contains__(self, key):
        '''
        '''
        
        return self.has_key(key)    
    
    def get_last_reset_time(self):
        '''
        '''
        
        return self._last_reset_time
    
    def keys(self):
        '''
        Returns all keys stored in current cache.

        @return: [object]
        '''
        
        raise NotImplementedError()
    
    def values(self):
        '''
        Returns all values stored in current cache.
        
        @return: [object]
        '''
        
        raise NotImplementedError()
        
    def update(self, E, **F):
        '''
        '''

        raise NotImplementedError()
