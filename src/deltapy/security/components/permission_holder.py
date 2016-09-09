'''
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.permission_holder import PermissionHolder
from deltapy.application.decorators import register
from deltapy.security import PERMISSION_HOLDER

@register(PERMISSION_HOLDER)
class PermissionHolderComponent(PermissionHolder):
    '''
    '''