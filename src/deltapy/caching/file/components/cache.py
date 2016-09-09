'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.caching.file.cache import FileCache
from deltapy.core import DeltaObject
from deltapy.application.decorators import register
import deltapy.caching.services as caching_services

@register(FileCache.CACHE_TYPE_NAME)
class FileCacheComponent(DeltaObject):
    '''
    '''
    
    def __init__(self):
        
        caching_services.register_cache_type(FileCache.CACHE_TYPE_NAME, FileCache)
        