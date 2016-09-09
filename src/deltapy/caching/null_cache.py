'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.caching.cache import CacheBase

class NullCache(CacheBase):
    '''
    A hash supported dictionary.
    '''

    CACHE_TYPE_NAME = 'null_cache'

    def set(self, key, value):
        '''
        Sets new value or updates existing value in cache.
        
        @param key: key
        @param value: value
        '''
        pass

    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''
        return 0      

    def has_key(self, key):
        return False
        
    def get(self, key, default = None):
        return default   
            
    def get_items(self):
        '''
        '''
        
        return []

    def keys(self):
        '''
        Returns all keys stored in current cache.
        '''
        return []
    
    def values(self):
        '''
        Returns all values stored in current cache.
        '''
        return []

    def reset_item(self, key):
        pass
        
    def clear(self):
        pass
    
    def reset(self):
        pass
