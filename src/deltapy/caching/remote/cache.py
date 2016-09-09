'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import cPickle
from multiprocessing import Lock

from deltapy.caching.cache import CacheBase
from deltapy.caching.remote.provider import RemoteCacheProvider

class RemoteCache(CacheBase):
    '''
    Remote cache class.
    '''
    
    CACHE_TYPE_NAME = 'remote_cache'
    
    def __init__(self, cache_name, **options):
        CacheBase.__init__(self, cache_name, **options)
        self._remote_cache_provider = RemoteCacheProvider()
        self._connection = self._remote_cache_provider.get_connection()
        self._lock = Lock()
        
    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''      
        
        return self._connection.execute('cache.len', self.get_name())
    
    def remove(self, key):
        '''
        Removes specified item from cache. 
        
        @param key: item key
        '''
        
        return self._connection.execute('cache.remove', self.get_name(), key)

    def get_id(self):
        '''
        Returns cache id.
        
        @return: object
        '''
        try:
            self._lock.acquire()
            
            return self._connection.execute('cache.len', self.get_name())
        finally:
            self._lock.release()
    
    def set_size(self, size):
        '''
        Sets cache size.
        
        @param size: cache new size 
        '''       
        
        return self._connection.execute('cache.set_size', self.get_name(), size)        
        
    def get_size(self):
        '''
        Returns cache size.
        
        @return: int
        '''
        
        return self._connection.execute('cache.get_size', self.get_name())

    def reset_item(self, key):
        '''
        Resets cache item.
        '''
        
        return self._connection.execute('cache.reset_item', self.get_name(), key)


    def clear(self):
        '''
        Removes all cache items.
        '''
        
        return self._connection.execute('cache.clear', self.get_name())
    
    def reset(self):
        '''
        Resets the cache.
        '''
        
        return self._connection.execute('cache.reset', self.get_name())

        
    def set(self, key, value):
        '''
        Sets given item using specified key.
        
        @param key: item key
        @param value: item value
        '''
        
        try:
            self._lock.acquire()
            _value = cPickle.dumps(value)
            return self._connection.execute('cache.set', self.get_name(), key, _value)
        finally:
            self._lock.release()

        
    def get(self, key, default = None):
        '''
        Gets given item using specified key.
        
        @param key: item key
        @return : object
        '''
        
        try:
            self._lock.acquire()
            value = self._connection.execute('cache.get', self.get_name(), key)
            if value is not None:
                deserialized_value = cPickle.loads(value)
                if deserialized_value is None:
                    return default
                return deserialized_value
            return value
        finally:
            self._lock.release()
    
    def has_key(self, key):
        '''
        Checks if given key is exist or not.
        
        @param key: item key
        @return: bool
        '''
        try:
            self._lock.acquire()
            return self._connection.execute('cache.has_key', self.get_name(), key)
        finally:
            self._lock.release()
        
    def get_items(self):
        '''
        Returns all items in cache.
        
        @return: [object]
        '''
        
        items = []
        for item in self._connection.execute('cache.get_items', self.get_name()):
            item.value = cPickle.loads(item.value)
            items.append(item)
        return items 

    def keys(self):
        '''
        Returns all keys.
        
        @return: [object]
        '''
        
        return self._connection.execute('cache.keys', self.get_name())

    def values(self):
        '''
        Returns all values.
        
        @return: [object]
        '''
        
        values = self._connection.execute('cache.values', self.get_name())
        results = []
        for value in values:
            results.append(cPickle.loads(value))
        return results 
        
    def get_last_reset_time(self):
        '''
        Returns last reset time of the cache.
        
        @return: float
        '''
        
        
        return self._connection.execute('cache.get_last_reset_time', self.get_name())
            
    def _get_cache_item_(self, key):
        
        return self._connection.execute('cache._get_cache_item_', self.get_name(), key)
    
        
