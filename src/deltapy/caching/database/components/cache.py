'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject
from deltapy.application.decorators import register
import deltapy.caching.services as caching_services
from deltapy.caching.database.cache import DatabaseCache

@register(DatabaseCache.CACHE_TYPE_NAME)
class DatabaseCacheComponent(DeltaObject):
    '''
    '''
    
    def __init__(self):
        caching_services.register_cache_type(DatabaseCache.CACHE_TYPE_NAME, 
                                             DatabaseCache)