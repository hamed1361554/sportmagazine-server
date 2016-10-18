'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.security.services as security_services
from deltapy.commander.decorators import command

@command('security.user.permissions')
def get_user_permissions(id):
    '''
    Returns all permissions of specified user.
    
    @param id: user ID
    
    @return: [permission info as DynamicObject]
    '''

    return security_services.get_user_permissions(id)

@command('security.user.create')
def create_user(id, password, fullname, **options):
    '''
    Creates a new user.
    
    @param id: user ID
    @param password: password
    @param fullname: full name
    @param **options: 
    '''

    return security_services.create_user(id, password, fullname, **options)

@command('security.user.remove')
def remove_user(id):
    '''
    Removes the given user.
    
    @param id: user name
    '''
    
    return security_services.remove_user(id)

@command('security.user.update')
def update_user(id, **params):
    '''
    Updates specified user with given parameters.
    
    @param id: user name
    @param **options: 
    '''

    return security_services.update_user(id, **params)

@command('security.user.get')
def get_user(id, **options):
    """
    Returns user information by specified name
    
    @param id: user name
    @keyword bool get_extra_user_info: extra user info should be gotten
                                           if this options is true.
    
    @return: user data as DynamicObject
    """
    return security_services.get_user(id, **options)

@command('security.user.activate')
def activate_user(id, flag):
    '''
    Active or inactive specified user. 
    
    @param id: user ID
    @param flag: activation flag(True or False)
    '''
    
    return security_services.activate_user(id, flag)

@command('security.user.is_superuser')
def is_superuser(id):
    '''
    Returns True if specified user is supper user else returns False
    
    @param id: user name
    
    @return: bool
    '''
    
    return security_services.is_superuser(id)

@command('security.user.is_active')
def is_active(user_id):
    '''
    Returns True if user is active.
    
    @param user_id: user ID
    
    @return: bool
    '''
    
    return security_services.is_active(user_id)

@command('security.user.is_expired')
def is_expired(user_id):
    '''
    Returns True if user is expired.
    
    @param user_id: user ID
    
    @return: bool
    '''
    
    return security_services.is_expired(user_id)

@command('security.user.all')
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
    
    return security_services.get_users(**options)

@command('security.role.create')
def create_role(name, **options):
	'''
	Creates a new role.

	@param id: role ID
	@param name: role name 
	@param **options: Other options.
	'''

	return security_services.create_role(name, **options)

@command('security.role.find')
def find_role(**options):
	'''
	Finds role according to given options.

    @param **options: Filters of find.

    @return: List of DynamicObject
	'''
	return security_services.find_role(**options)
    	
@command('security.role.save')
def add_or_update_role(code, **options):
    '''
    Adds or updates role.
    
    @param code: role code
    @param **options:
    '''
    
    return security_services.add_or_update_role(code, **options)

@command('security.role.remove')
def remove_role(code):
    '''
    Removes specified role.
    
    @param code: role code
    '''
    
    return security_services.remove_role(code)

@command('security.role.update')
def update_role(code, **params):
    '''
    Removes specified role.
    
    @param code: role code
    @param **params: 
    '''
    
    return security_services.update_role(code, **params)

@command('security.role.get')
def get_role(code, **options):
    '''
    Returns role information by given role code.
    
    @param code: role code
    @param **options: Other options.
    '''

    return security_services.get_role(code, **options)

@command('security.role.all')
def get_roles(**options):
    '''
    Returns roles considering given options.
    
    @param **options:
        user_id: user ID
    
    @return: [DynamicObject<...>]
    '''

    return security_services.get_roles(**options)

@command('security.role.assign')
def assign_role(user_id, role_ids):
    '''
    Assigns given roles to specified user.
    
    @param user_id: user ID
    @param role_ids: list role ID
    '''
    
    return security_services.assign_role(user_id, role_ids)

@command('security.role.unassign')
def unassign_role(user_id, role_ids):
    '''
    Unassigns given roles from specified user.
    
    @param user_id: user ID
    @param role_ids: list role ID
    '''
    
    return security_services.unassign_role(user_id, role_ids)

@command('security.permission.create')
def create_permission(id, name, **options):
    '''
    Creates a new permission.
    @param id: permission ID
    @param name: permission name
    @param **options: 
    '''
    
    return security_services.create_permission(id, name, **options)

@command('security.permission.save')
def add_or_update_permission(id, **options):
    '''
    Adds new permission or updates existed permission.
    @param id: permission ID
    '''

    return security_services.add_or_update_permission(id, **options)
    
@command('security.permission.remove')
def remove_permission(id):
    '''
    Removes specified permission.
    
    @param id: permission ID
    '''
    
    return security_services.remove_permission(id)

@command('security.permission.update')
def update_permission(id, **params):
    '''
    Updates specified permission using given parameters. 
    @param id: permission ID
    @param **params: 
    '''
    
    return security_services.update_permission(id, **params)

@command('security.permission.get')
def get_permission(id):
    '''
    Returns specified permission information.
    @param id:
    '''
    
    return security_services.get_permission(id)

@command('security.permission.all')
def get_permissions(**options):
    '''
    Returns a list of permission considering given options.
    
    @param **options:
        role_id: role ID
    '''
    
    return security_services.get_permissions(**options)

@command('security.permission.grant')
def grant_permission(role_id, permission_ids):
    '''
    Grants given permissions.
    
    @param role_id: role ID
    @param permission_ids: list of permission ID
    '''
    
    return security_services.grant_permission(role_id, permission_ids)

@command('security.permission.deny')
def deny_permission(role_id, permission_ids):
    '''
    Denies given permissions.
    
    @param role_id: role ID
    @param permission_ids: list of permission ID
    '''

    return security_services.deny_permission(role_id, permission_ids)
    
@command('security.password.reset')
def reset_password(user_id, new_password):
    '''
    Resets password of the given user to new password.
    
    @param user_id: user ID
    @param new_password: user new password 
    '''

    return security_services.reset_password(user_id, new_password)

@command('security.password.change')
def change_password(current_password, new_password):
    '''
    Changes password of current user.
    
    @param current_password: user current password
    @param new_password: user new password 
    '''

    return security_services.change_password(current_password, new_password)

@command('security.user.roles')
def get_user_roles(user_id, **options):
    '''
    Returns all roles which are assigned to specified user.
    
    @param user_id: user ID
    @param **options: 
    
    @return: [role as DynamicObject]
    '''
    
    return security_services.get_user_roles(user_id, **options)

@command('security.role.permissions')
def get_role_permissions(role_id, **options):
    '''
    Returns all permissions which are granted to specified role.
    
    @param role_id: role ID
    
    @return: [permission as DynamciObject]
    '''

    return security_services.get_role_permissions(role_id, **options)

@command('security.role.users')
def get_role_users(role_id, **options):
    '''
    Returns all user which is assigned to specified role.
    
    @param role_id: role ID
    
    @return: [user as DynamicObject]
    '''
    
    return security_services.get_role_users(role_id, **options)

@command('security.permission.roles')
def get_permission_roles(permission_id, **options):
    '''
    Returns all roles which are including specified permission.
    
    @param permission_id: permission ID
    
    @return: [role as DynamicObject]
    '''

    return security_services.get_permission_roles(permission_id, **options)
