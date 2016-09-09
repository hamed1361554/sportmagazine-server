'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

from threading import Lock

from deltapy.core import DeltaObject, DeltaException
from deltapy.caching.memory_cache import MemoryCache
import deltapy.config.services as config_services
from deltapy.caching.null_cache import NullCache

class CacheManagerException(DeltaException):
    '''
    A class for handling cache errors.
    '''
    pass

class CacheManager(DeltaObject):
    '''
    Provide management on cache objects.
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        self.caches = {}
        self.cache_lock = Lock()
        
        self._registered_cache_types = {}
        self._default_cache_type_name = None 
        self.register_cache_type(MemoryCache.CACHE_TYPE_NAME, MemoryCache)
        self.register_cache_type(NullCache.CACHE_TYPE_NAME, NullCache)
        
    def set_default_cache_type_name(self, cache_type_name):
        '''
        Sets default cache type.
        
        @param cache_type_name: cache type name 
        '''
        
        self._default_cache_type_name = cache_type_name
        
    def get_default_cache_type_name(self):
        '''
        Returns default cache type

        @return: str
        '''
        
        if self._default_cache_type_name is None:
            try:
                config_store = config_services.get_app_config_store('caching')
                self._default_cache_type_name = config_store.get('global', 'default')
            except:
                self._default_cache_type_name = MemoryCache.CACHE_TYPE_NAME
        return self._default_cache_type_name
        
    def get_config_data(self, cache_type_name):
        '''
        Returns configuration data for specified cache.
        
        @param cache_type_name: cache type name
        
        @return: DynamicObject
        '''

        try:
            config_store = config_services.get_app_config_store('caching')
            return config_store.get_section_data(cache_type_name)
        except:
            return {}
    
    def get_cache(self, name, cache_type_name = None, **cache_params):
        '''
        Returns the cache by given name. If the cache does not exists,
        This function creates a new cache by the given name and returns it.
        
        @param name: cache name.
        @param cache_type_name: type of cache.
        @param **cache_params: required parameters of specified cache type.  
        @return: Cache        
        '''
        
        if not self.caches.has_key(name):
            _cache_type_name = self.get_default_cache_type_name()
            if cache_type_name is not None:
                _cache_type_name = cache_type_name
            config_params = self.get_config_data(_cache_type_name)
            config_params.update(cache_params)
            if not config_params.get('enable', True):
                return NullCache(name, **cache_params)
            cache_type = self.get_cache_type(_cache_type_name)
            self.add_cache(cache_type(name, **config_params))
        return self.caches[name]
    
    def register_cache_type(self, name, cache_type):
        '''
        Registers a cache type using specified name.
        @param name: registration name.
        @param type: class type.
        '''
        self._registered_cache_types[name] = cache_type
    
    def get_cache_type(self, cache_type_name):
        '''
        Returns registered cache type.
        
        @param type_type_name: cache type name
        
        @return: Cache class type
        '''
        
        cache_type = self._registered_cache_types.get(cache_type_name)
        if cache_type is None:
            message = _('Cache type [{cache_type_name}] not registered.')
            raise CacheManagerException(message.format(cache_type_name = cache_type_name))
        return cache_type

    def add_cache(self, cache, replace = False):
        '''
        Adds the cache to caches container.
        If replace flag is True then the existing cache replaces with this cache.
        
        @param cache: cache object
        @param replace: replace flag
        '''
        try:
            self.cache_lock.acquire()
            if self.caches.has_key(cache.get_name()):
                if not replace:
                    raise CacheManagerException('A cache named[%s] is already existed.' % cache.get_name())
            self.caches[cache.get_name()] = cache
        finally:
            self.cache_lock.release()
                
    def reset_cache(self, name):
        '''
        Resets a cache.
        
        @param name: cache name
        '''
        if self.caches.has_key(name):
            cache = self.caches[name]
            cache.reset()
        
    def drop_cache(self, name):
        '''
        Drops a cache. In facts removes the cache object from caches container.

        @param name: cache name
        '''
        try:
            self.cache_lock.acquire()
            if self.caches.has_key(name):
                self.caches.pop(name)
        finally:
            self.cache_lock.release()
            
    def get_caches(self):
        '''
        Returns all caches in container.
        
        @return: list<Cache>
        '''
        return self.caches.values()

    def exists(self, name):
        '''
        Returns True if cache exists in cache manager.
        
        @return: bool
        '''

        return name in self.caches
        
