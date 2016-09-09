'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject
from deltapy.application.decorators import register
from deltapy.caching.remote.cache import RemoteCache
import deltapy.caching.services as caching_services

@register(RemoteCache.CACHE_TYPE_NAME)
class RomteCacheComponent(DeltaObject):
    '''
    '''
    
    def __init__(self):
        caching_services.register_cache_type(RemoteCache.CACHE_TYPE_NAME, RemoteCache)