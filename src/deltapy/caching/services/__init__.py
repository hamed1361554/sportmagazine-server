'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

from deltapy.locals import get_app_context, APP_CACHING

def get_cache(name, cache_type_name = None, **cache_params):
    '''
    Returns the cache by given name. If the cache does not exists,
    This function creates a new cache by the given name and returns it.
    
    @param name: cache name.
    @param cache_type_name: type of cache.
    @param **cache_params: required parameters of specified cache type.  
    @return: Cache        
    '''          
    return get_app_context()[APP_CACHING].get_cache(name, cache_type_name, **cache_params)

def add_cache(cache, replace = False):
    return get_app_context()[APP_CACHING].add_cache(cache, replace)

def reset_cache(name):
    return get_app_context()[APP_CACHING].reset_cache(name)

def drop_cache(name):
    return get_app_context()[APP_CACHING].drop_cache(name)
    
def get_caches():
    return get_app_context()[APP_CACHING].get_caches()

def register_cache_type(name, cache_type):
    '''
    Registers a cache type using specified name.
    @param name: registration name.
    @param type: class type.
    '''
    return get_app_context()[APP_CACHING].register_cache_type(name, cache_type)

def exists(name):
    '''
    Returns True if cache exists in cache manager.

    @return: bool
    '''

    return get_app_context()[APP_CACHING].exists(name)
    
