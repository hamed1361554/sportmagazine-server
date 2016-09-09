'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
import hashlib
import cPickle
import time
import multiprocessing

from deltapy.caching.cache import CacheBase, CacheItem, CacheException
from deltapy.utils.concurrent import LockedArea

class FileCache(CacheBase):
    '''
    Provides caching in file system.
    '''
    
    CACHE_TYPE_NAME = 'file_cache'
    
    def __init__(self, cache_name, **options):
        CacheBase.__init__(self, cache_name, **options)
        
        self._dir = options.get('dir', '/tmp')
        # Checking directory
        if not os.path.exists(self._dir):
            os.mkdir(self._dir)
            
        # Creating hashed file name
        self._filename = hashlib.md5(cache_name).hexdigest()
        # Setting file full path 
        self._filepath = os.path.join(self._dir, self._filename)
        
        # Creating lock object
        self._lock = multiprocessing.Lock()
        
        # Creating cache file
        self.clear()
        
    def _load_dict_object_(self):
        '''
        Returns dictionary object which is saved in file. 
        '''
        
        file = open(self._filepath, 'rb')
        obj = cPickle.load(file)
        file.close()
        return obj
        
    def _save_dict_object_(self, obj):
        '''
        Saves dictionary object in file.
        '''
        
        file = open(self._filepath, 'wb')
        cPickle.dump(obj, file)
        file.close()
        
    
    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''
        
        items, old_items = self._load_dict_object_()
        return len(items) + len(old_items)
    
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
        
        self._size = size
        
        
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

        with LockedArea(self._lock):
            
            # Loading cache entire
            items, old_items = self._load_dict_object_()
            
            cache_item = items.get(key)
            
            if not cache_item:
                cache_item = old_items.get(key, None)
                
            if cache_item:
                cache_item.last_reset_time = time.time()
                cache_item.expired = True
                
            self._save_dict_object_((items, old_items))

    def clear(self):
        '''
        Removes all cache items.
        '''

        with LockedArea(self._lock):
            items = {}
            old_items = {}
            self._save_dict_object_((items, old_items))
    
    def reset(self):
        '''
        Resets the cache.
        '''
        
        with LockedArea(self._lock):
            last_reset_time = time.time()
            
            items, old_items = self._load_dict_object_()
            
            for cache_item in items.values():
                cache_item.last_reset_time = last_reset_time
                cache_item.expired = True

            for cache_item in old_items.values():
                cache_item.last_reset_time = last_reset_time
                cache_item.expired = True

            self._last_reset_time = last_reset_time
            
            self._save_dict_object_((items, old_items))
        
    def set(self, key, value):
        '''
        Sets new value or updates existing value in cache.
        
        @param key: key
        @param value: value
        '''
        
        with LockedArea(self._lock):
            items, old_items = self._load_dict_object_()
            cache_item = items.get(key)
            if not cache_item:            
                cache_item = CacheItem(key, value)
                max_size = self.get_size()
                if max_size > 0 and len(items) >= max_size:
                    items, old_items = old_items, items
                    items.clear()
                items[key] = cache_item
            else: 
                cache_item.last_reset_time = time.time()
                cache_item.value = value
                cache_item.expired = False
            self._save_dict_object_((items, old_items))
            
    def remove(self, key):
        '''
        Removes specified item from cache. 
        
        @param key: item key
        '''
        
        with LockedArea(self._lock):
            items, old_items = self._load_dict_object_()
            if key in items:
                del items[key]
            elif key in old_items:
                del old_items[key]
            self._save_dict_object_((items, old_items))
        

    def _check_lifetime_(self, cache_item):                
        '''
        Checks item life time.
       
        @param cache_item: cache item
        
        @return: CacheItem
        '''
        
        scavenger = self.get_scavenger()
        
        if scavenger:
            scavenger.scavenge(self, cache_item)
            
        return cache_item
        
    def get(self, key, default = None):
        '''
        Returns value considering key.
        
        @param key: key
        @param [default]: returns default value if items not exists.(default is None)
        
        @return: object
        '''
        
        items, old_items = self._load_dict_object_()

        cache_item = items.get(key)
        if cache_item is None:
            cache_item = old_items.get(key)
        if cache_item is None:
            return default

        cache_item =  self._check_lifetime_(cache_item)       
        
        if cache_item.expired:
            cache_item.miss_count += 1
            with LockedArea(self._lock):
                self._save_dict_object_((items, old_items))
            raise CacheException('Item [%s] is expired in cache[%s]' % (key, self.get_name()))
        
        return cache_item.value
    
    def has_key(self, key):
        '''
        Returns True if key exists in cache.
        
        @return:  bool
        '''
        
        items, old_items = self._load_dict_object_()

        cache_item = items.get(key)
        if cache_item is None:
            cache_item = old_items.get(key)
        if cache_item is None:
            return False
        
        cache_item =  self._check_lifetime_(cache_item)       
        
        if cache_item.expired:
            with LockedArea(self._lock):
                self._save_dict_object_((items, old_items))
            raise CacheException('Item [%s] is expired in cache[%s]' % (key, self.get_name()))
        
        return True
        
    def get_items(self):
        '''
        Returns all cache items in cache.
        
        @return: [CacheItem]
        '''
        
        items, old_items = self._load_dict_object_()
        return items.values() + old_items.values()
        
    def keys(self):
        '''
        Returns all keys stored in current cache.
        '''
    
        items, old_items = self._load_dict_object_()
        return items.keys() + old_items.keys()

    def values(self):
        '''
        Returns all values stored in current cache.
        '''

        items = self.get_items()
        return [item.value for item in items if not item.expired]
