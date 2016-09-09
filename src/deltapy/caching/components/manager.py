'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.caching.manager import CacheManager
from deltapy.application.decorators import register
import deltapy.locals


@register(deltapy.locals.APP_CACHING)
class CacheManagerComponent(CacheManager):
    '''
    Just for registering in deltapy.
    '''
