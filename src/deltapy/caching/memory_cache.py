'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import time
from copy import deepcopy
from multiprocessing import Lock

from deltapy.caching.cache import CacheBase, CacheItem, CacheException

class MemoryCacheException(CacheException):
    '''
    '''

class MemoryCache(CacheBase):
    '''
    A hash supported dictionary.
    '''
    
    CACHE_TYPE_NAME = 'memory_cache'

    def __init__(self, cache_name, **options):
        CacheBase.__init__(self, cache_name, **options)
        
        self._old_items = {}
        self._items = {}
        self._cache_lock = Lock()
        
    def set(self, key, value):
        '''
        Sets new value or updates existing value in cache.
        
        @param key: key
        @param value: value
        '''
        
        if self.get_size() <= 0:
            return

        value = deepcopy(value)

        try:
            self._cache_lock.acquire()
            cache_item = self._items.get(key, None)
            if not cache_item:            
                cache_item = CacheItem(key, value)
                if len(self._items) >= self.get_size():
                    self._items, self._old_items = self._old_items, self._items
                    self._items.clear()
                self._items[key] = cache_item 
            else: 
                cache_item.last_reset_time = time.time()
                cache_item.value = value
                cache_item.expired = False                
        except Exception, error:
            raise MemoryCacheException('Error[%s] occurred in cache[%s]' % (error, 
                                                                      self.get_name()))
        finally:
            self._cache_lock.release()

    def remove(self, key):
        '''
        Removes specified item from cache. 
        
        @param key: item key
        '''
        
        if key in self._items:
            del self._items[key]
        elif key in self._old_items:
            del self._old_items[key]

    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''      
        return len(self._items)


    def has_key(self, key):
        cache_item = self._check_lifetime_(key)      
        
        if cache_item is not None and not cache_item.expired:
            return True
        
        return False
        
    def get(self, key, default = None):   
        
        if key not in self._items:
            if key not in self._old_items:
                return default
        
        cache_item =  self._check_lifetime_(key)       
        
        if not cache_item:
            raise MemoryCacheException('Item [%s] not found in cache[%s]' % (key, self.get_name()))
        elif cache_item.expired:
            cache_item.miss_count += 1
            raise MemoryCacheException('Item [%s] is expired in cache[%s]' % (key, self.get_name()))
        
        cache_item.hit_count += 1
        
        return deepcopy(cache_item.value)
            
    def _check_lifetime_(self, key):
        
        cache_item = self._items.get(key)
        
        if cache_item is None:
            cache_item = self._old_items.get(key)
            if not cache_item:
                return None
        
        scavenger = self.get_scavenger()
        
        if scavenger is not None:
            scavenger.scavenge(self, cache_item)
            
        return cache_item

    def get_items(self):
        '''
        '''
        
        return self._old_items.values() + self._items.values()

    def keys(self):
        '''
        Returns all keys stored in current cache.
        '''
        keys = []
        for cache_item in self.get_items():
            keys.append(cache_item.key)
        return keys
    
    def values(self):
        '''
        Returns all values stored in current cache.
        '''
        values = []
        for cache_item in self.get_items():
            values.append(deepcopy(cache_item.value))
        return values

    def reset_item(self, key):
        cache_item = self._items.get(key, None)
        
        if not cache_item:
            cache_item = self._old_items.get(key, None)
            
        if cache_item :
            cache_item.last_reset_time = time.time()
            cache_item.expired = True

    def clear(self):
        self._old_items.clear()
        self._items.clear()
    
    def reset(self):
        try:
            self._cache_lock.acquire()
            
            last_reset_time = time.time()
            
            for cache_item in self._items.values():
                cache_item.last_reset_time = last_reset_time
                cache_item.expired = True

            for cache_item in self._old_items.values():
                cache_item.last_reset_time = last_reset_time
                cache_item.expired = True
            
            self._last_reset_time = last_reset_time
        finally:
            self._cache_lock.release()  

    def update(self, E, **F):
        '''
        '''
        
        self._old_items = {}
        self._items.update(E, **F)
