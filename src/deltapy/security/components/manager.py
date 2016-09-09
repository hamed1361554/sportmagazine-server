'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.manager import BaseSecurityManager
from deltapy.application.decorators import register
from deltapy.locals import APP_SECURITY

@register(APP_SECURITY)
class BaseSecurityManagerComponent(BaseSecurityManager):
    '''
    Just for integration with deltapy.
    '''