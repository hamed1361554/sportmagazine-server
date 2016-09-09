'''
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security import PERMISSION_HOLDER

def hold(permission):
    '''
    Holds the permission.
    
    @param permission: permission instance
    '''

    return get_component(PERMISSION_HOLDER).hold(permission)
    
def get_permissions():
    '''
    Returns all permissions in holder.
    
    @return: [Permission]
    '''
    
    return get_component(PERMISSION_HOLDER).get_permissions()

def sync(**options):
    '''
    Synchronizes permissions with database.

    @param **options:
       options to pass along with this command.
    '''
    
    return get_component(PERMISSION_HOLDER).sync(**options)
