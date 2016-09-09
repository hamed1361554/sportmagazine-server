'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.security.authorization.services as authorization_services 

@command('security.authorize')
def authorize(user_id, permission_ids):
    '''
    Authorizes user for permissions.
    
    @param user_id: user ID
    @param permission_ids: list of permission ID 
    '''
    
    return authorization_services.authorize(user_id, permission_ids)
    
@command('security.is_in_role')
def is_in_role(permission_ids, user_id=None):
    '''
    Returns True if current user has permissions.
     
    @param permission_ids: list of permission ID
    @param user_id: user_id to check it's roles
    
    @return: bool
    '''
    
    return authorization_services.is_in_role(permission_ids, user_id=user_id)
