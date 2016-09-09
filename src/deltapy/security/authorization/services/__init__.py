'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.event_system.decorators import delta_event
from deltapy.security.authorization import APP_AUTHORIZER


@delta_event('security.authorize')
def authorize(user_id, permission_ids):
    '''
    Authorizes user for permissions.
    
    @param user_id: user ID
    @param permission_ids: list of permission ID 
    '''
    
    return get_component(APP_AUTHORIZER).authorize(user_id, permission_ids)
    
def is_in_role(permission_ids, user_id=None):
    '''
    Returns True if current user has permissions.
     
    @param permission_ids: list of permission ID
    @param user_id: user_id to check it's roles
    
    @return: bool
    '''
    
    return get_component(APP_AUTHORIZER).is_in_role(permission_ids, user_id=user_id)
