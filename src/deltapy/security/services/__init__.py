'''
Created on Aug 10, 2009

@author: mohammadi
'''
from deltapy.application.services import get_component
from deltapy.locals import APP_SECURITY

def get_user_permissions(id):
    '''
    Returns all permissions of specified user.
    
    @param id: user ID
    
    @return: [permission info as DynamicObject]
    '''

    return get_component(APP_SECURITY).get_user_permissions(id)

def create_internal_user(id, **options):
    '''
    Create an internal user.
    
    @param id: user ID
    '''
    
    return get_component(APP_SECURITY).create_internal_user(id, **options)

def create_user(id, password, fullname, **options):
    '''
    Creates a new user.
    
    @param id: user ID
    @param password: password
    @param fullname: full name
    @param **options: 
    '''

    return get_component(APP_SECURITY).create_user(id, password, fullname, **options)

def remove_user(id):
    '''
    Removes the given user.
    
    @param id: user name
    '''
    
    return get_component(APP_SECURITY).remove_user(id)

def update_user(id, **params):
    '''
    Updates specified user with given parameters.
    
    @param id: user name
    @param **options: 
    '''

    return get_component(APP_SECURITY).update_user(id, **params)

def get_user(id, **options):
    """
    Returns user information by specified name
    
    @param id: user name
    @keyword bool get_extra_user_info: extra user info should be gotten
                                       if this options is true.
    
    @return: user data as DynamicObject
    """
    
    return get_component(APP_SECURITY).get_user(id, **options)


def get_user_by_id(user_id, **options):
    """
    Returns user information by specified name

    @param user_id: user ID

    @return: user data as DynamicObject
    """

    return get_component(APP_SECURITY).get_user_by_id(user_id, **options)

def activate_user(id, flag, **optios):
    '''
    Active or inactive specified user. 
    
    @param id: user ID
    @param flag: activation flag(True or False)
    '''
    
    return get_component(APP_SECURITY).activate_user(id, flag, **optios)


def is_superuser(id):
    '''
    Returns True if specified user is supper user else returns False
    
    @param id: user name
    
    @return: bool
    '''
    
    return get_component(APP_SECURITY).is_superuser(id)

def is_active(user_id):
    '''
    Returns True if user is active.
    
    @param user_id: user ID
    
    @return: bool
    '''
    
    return get_component(APP_SECURITY).is_active(user_id)

def is_expired(user_id):
    '''
    Returns True if user is expired.
    
    @param user_id: user ID
    
    @return: bool
    '''
    
    return get_component(APP_SECURITY).is_expired(user_id)

def get_users(**options):
    '''
    Returns users using given options.
    
    @param **options: 
        id: user ID
        fullname: user full name
        is_active: user activation flag
        is_superuser: supper user determination flag

    @return: [DynamicObject<user info...>]
    '''
    
    return get_component(APP_SECURITY).get_users(**options)

def create_role(name, **options):
    '''
    Creates a new role.
    
    @param id: role ID
    @param name: role name 
    @param **options: Other options.
    '''

    return get_component(APP_SECURITY).create_role(name, **options)

def find_role(**options):
    '''
    Finds role according to given options.

    @param **options:
    @param **options: Filters of find.

    @return: List of DynamicObject
    '''
   
    return get_component(APP_SECURITY).find_role(**options)
   
def add_or_update_role(code, **options):
    '''
    Adds or updates role.
    
    @param code: role code
    @param **options:
    '''
    
    return get_component(APP_SECURITY).add_or_update_role(code, **options)

def remove_role(code):
    '''
    Removes specified role.
    
    @param code: role code
    '''
    
    return get_component(APP_SECURITY).remove_role(code)

def update_role(code, **params):
    '''
    Removes specified role.
    
    @param code: role code
    @param **params: 
    '''
    
    return get_component(APP_SECURITY).update_role(code, **params)

def get_role(code, **options):
    '''
    Returns role information by given role code.
    
    @param code: role code
    @param **options: Other options.
    '''

    return get_component(APP_SECURITY).get_role(code, **options)

def get_roles(**options):
    '''
    Returns roles considering given options.
    
    @return: [DynamicObject<...>]
    '''

    return get_component(APP_SECURITY).get_roles(**options)

def assign_role(user_id, role_ids):
    '''
    Assigns given roles to specified user.
    
    @param user_id: user ID
    @param role_ids: list role ID
    '''
    
    return get_component(APP_SECURITY).assign_role(user_id, role_ids)

def unassign_role(user_id, role_ids):
    '''
    Unassigns given roles from specified user.
    
    @param user_id: user ID
    @param role_ids: list role ID
    '''
    
    return get_component(APP_SECURITY).unassign_role(user_id, role_ids)

def create_permission(id, name, **options):
    '''
    Creates a new permission.
    @param id: permission ID
    @param name: permission name
    @param **options: 
    '''
    
    return get_component(APP_SECURITY).create_permission(id, name, **options)

def add_or_update_permission(id, **options):
    '''
    Adds new permission or updates existed permission.
    @param id: permission ID
    '''

    return get_component(APP_SECURITY).add_or_update_permission(id, **options)
    
def remove_permission(id):
    '''
    Removes specified permission.
    
    @param id: permission ID
    '''
    
    return get_component(APP_SECURITY).remove_permission(id)

def update_permission(id, **params):
    '''
    Updates specified permission using given parameters. 
    @param id: permission ID
    @param **params: 
    '''
    
    return get_component(APP_SECURITY).update_permission(id, **params)

def get_permission(id):
    '''
    Returns specified permission information.
    @param id:
    '''
    
    return get_component(APP_SECURITY).get_permission(id)

def get_permissions(**options):
    '''
    Returns a list of permission considering given options.
    '''
    
    return get_component(APP_SECURITY).get_permissions(**options)

def grant_permission(role_id, permission_ids):
    '''
    Grants given permissions.
    
    @param role_id: role ID
    @param permission_ids: list of permission ID
    '''
    
    return get_component(APP_SECURITY).grant_permission(role_id, permission_ids)

def deny_permission(role_id, permission_ids):
    '''
    Denies given permissions.
    
    @param role_id: role ID
    @param permission_ids: list of permission ID
    '''

    return get_component(APP_SECURITY).deny_permission(role_id, permission_ids)
    

def encrypt_password(id, password, **options):
    '''
    Encrypts the given password.
    
    @param id: user ID
    @param password: user password
    @param **options:
    
    @return: str 
    '''
    
    return get_component(APP_SECURITY).encrypt_password(id, password, **options)

def reset_password(user_id, new_password):
    '''
    Resets password of the given user to new password.
    
    @param user_id: user ID
    @param new_password: user new password 
    '''

    return get_component(APP_SECURITY).reset_password(user_id, new_password)

def change_password(user_id, current_password, new_password, **options):
    '''
    Changes password of current user.
    
    @param current_password: user current password
    @param new_password: user new password 
    '''

    return get_component(APP_SECURITY).change_password(user_id, current_password, new_password, **options)


def get_user_roles(user_id, **options):
    '''
    Returns all roles which are assigned to specified user.
    
    @param user_id: user ID
    @param **options: 
    
    @return: [role as DynamicObject]
    '''
    
    return get_component(APP_SECURITY).get_user_roles(user_id, **options)

def get_role_permissions(role_id, **options):
    '''
    Returns all permissions which are granted to specified role.
    
    @param role_id: role ID
    
    @return: [permission as DynamciObject]
    '''

    return get_component(APP_SECURITY).get_role_permissions(role_id, **options)

def get_role_users(role_id, **options):
    '''
    Returns all user which is assigned to specified role.
    
    @param role_id: role ID
    
    @return: [user as DynamicObject]
    '''
    
    return get_component(APP_SECURITY).get_role_users(role_id, **options)

def get_permission_roles(permission_id, **options):
    '''
    Returns all roles which are including specified permission.
    
    @param permission_id: permission ID
    
    @return: [role as DynamicObject]
    '''

    return get_component(APP_SECURITY).get_permission_roles(permission_id, **options)
