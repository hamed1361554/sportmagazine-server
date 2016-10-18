'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import hashlib

from deltapy.core import DeltaObject, DeltaException
import deltapy.logging.services as logging
import deltapy.security.session.services as session_services

class SecurityManagerException(DeltaException):
    '''
    For handling security manager errors.
    '''

class UserNotFoundException(SecurityManagerException):
    '''
    Raises when there's no such user.
    '''

class RoleNotFoundException(SecurityManagerException):
    '''
    Raises when the role is not defined in the system.
    '''

class PermissionNotFoundException(SecurityManagerException):
    '''
    When the specified permission not exist in the system.
    '''


class InternalUser(DeltaObject):
    '''
    '''
    
    def __init__(self, id):
        '''
        
        @param id:
        '''
        
        self.id = id
        self.fullname = None
    

class BaseSecurityManager(DeltaObject):
    '''
    Provides security functionality.
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)

    def encrypt_password(self, id, password, **options):
        '''
        Encrypts the given password.
        
        @param id: user ID
        @param password: user password
        @param **options:
        
        @return: str 
        '''
        
        return str(hashlib.sha512(password + id).hexdigest())

    def create_internal_user(self, id, **options):
        '''
        Create an internal user.
        
        @param id: user ID
        '''
        
        return InternalUser(id)

    def create_user(self, id, password, fullname, **options):
        '''
        Creates a new user.
        
        @param id: user ID
        @param password: password
        @param fullname: full name
        @param **options: 
        '''

        raise NotImplementedError()

    def remove_user(self, id):
        '''
        Removes the given user.
        
        @param id: user name
        '''
        
        raise NotImplementedError()

    def update_user(self, id, **params):
        '''
        Updates specified user with given parameters.
        
        @param id: user name
        @param **options: 
        '''

        raise NotImplementedError()
    
    def activate_user(self, id, flag):
        '''
        Active or inactive specified user. 
        
        @param id: user ID
        @param flag: activation flag(True or False)
        '''
        
        raise NotImplementedError()
    
    def is_active(self, user_id):
        '''
        Returns True if user is active.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        raise NotImplementedError()
    
    def is_expired(self, user_id):
        '''
        Returns True if user is expired.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        raise NotImplementedError()

    def get_user(self, id, **options):
        """
        Returns user information by specified name
        
        @param id: user name
        @keyword bool get_extra_user_info: extra user info should be gotten
                                           if this options is true.
        
        @return: user data as DynamicObject
        """
        
        raise NotImplementedError()


    def is_superuser(self, id):
        '''
        Returns True if specified user is supper user else returns False
        
        @param id: user name
        
        @return: bool
        '''
        
        raise NotImplementedError()

    def get_users(self, **options):
        '''
        Returns users using given options.
        
        @return: [DynamicObject<user info...>]
        '''
        
        raise NotImplementedError()
    
    def reset_password(self, user_id, new_password):
        '''
        Resets password of the given user to new password.
        
        @param user_id: user ID
        @param new_password: user new password 
        '''
        user = session_services.get_current_user()
        if not self.is_superuser(user.id):
            raise SecurityManagerException('You are not super user.')

        self.update_user(user_id, password = self.encrypt_password(user_id, new_password))

    def change_password(self, current_password, new_password):
        '''
        Changes password of current user.
        
        @param current_password: user current password
        @param new_password: user new password 
        '''
    
        user = session_services.get_current_user()
        if self.encrypt_password(user.id, current_password) != user.password:
            raise SecurityManagerException('Your password is incorrect.')
        
        self.update_user(user.id, password = self.encrypt_password(user.id, new_password))
        
    def create_role(self, name, **options):
        '''
        Creates a new role.
        
        @param id: role ID
        @param name: role name 
        @param **options: Other options.
        '''

        raise NotImplementedError()
    
    def find_role(self, **options):
        '''
        Finds role according to given options.

        @param **options: Filters of find.

        @return: List of DynamicObject
        '''
        raise NotImplementedError()

    def add_or_update_role(self, id, **options):
        '''
        Adds or updates role.
        
        @param id: role ID
        @param **options:
        '''
        
        raise NotImplementedError()

    def remove_role(self, id):
        '''
        Removes specified role.
        
        @param id: role ID
        '''
        
        raise NotImplementedError()

    def update_role(self, id, **params):
        '''
        Removes specified role.
        
        @param id: role ID
        @param **params: 
        '''
        
        raise NotImplementedError()

    def get_role(self, id, **options):
        '''
        Returns role information by given role ID.
        
        @param role_id: role ID
        @param **options: Other options.
        '''

        raise NotImplementedError()

    def get_roles(self, **options):
        '''
        Returns roles considering given options.
        
        @return: [DynamicObject<...>]
        '''

        raise NotImplementedError()
    
    def assign_role(self, user_id, role_ids):
        '''
        Assigns given roles to specified user.
        
        @param user_id: user ID
        @param role_ids: list role ID
        '''
        
        raise NotImplementedError()

    def unassign_role(self, user_id, role_ids):
        '''
        Unassigns given roles from specified user.
        
        @param user_id: user ID
        @param role_ids: list role ID
        '''
        
        raise NotImplementedError()

    def create_permission(self, id, name, **options):
        '''
        Creates a new permission.
        @param id: permission ID
        @param name: permission name
        @param **options: 
        '''
        
        raise NotImplementedError()
    
    def add_or_update_permission(self, id, **options):
        '''
        Adds new permission or updates existed permission.
        @param id: permission ID
        '''

        raise NotImplementedError()
        
    def remove_permission(self, id):
        '''
        Removes specified permission.
        
        @param id: permission ID
        '''
        
        raise NotImplementedError()

    def update_permission(self, id, **params):
        '''
        Updates specified permission using given parameters. 
        @param id: permission ID
        @param **params: 
        '''
        
        raise NotImplementedError()

    def get_permission(self, id):
        '''
        Returns specified permission information.
        @param id:
        '''
        
        raise NotImplementedError()
    
    def get_permissions(self, **options):
        '''
        Returns a list of permission considering given options.
        '''
        
        raise NotImplementedError()
    
    def grant_permission(self, role_id, permission_ids):
        '''
        Grants given permissions.
        
        @param role_id: role ID
        @param permission_ids: list of permission ID
        '''
        
        raise NotImplementedError()
    
    def deny_permission(self, role_id, permission_ids):
        '''
        Denies given permissions.
        
        @param role_id: role ID
        @param permission_ids: list of permission ID
        '''

        raise NotImplementedError()
    
    def get_user_roles(self, user_id, **options):
        '''
        Returns all roles which are assigned to specified user.
        
        @param user_id: user ID
        @param **options: 
        
        @return: [role as DynamicObject]
        '''
        
        return self.get_roles(user_id = user_id)
    
    def get_role_permissions(self, role_id, **options):
        '''
        Returns all permissions which are granted to specified role.
        
        @param role_id: role ID
        
        @return: [permission as DynamciObject]
        '''

        return self.get_permissions(role_id = role_id)
        
    def get_user_permissions(self, id):
        '''
        Returns all permissions of specified user.
        
        @param id: user ID
        
        @return: [permission info as DynamicObject]
        '''
        permissions = []
        for r in self.get_roles(user_id = id):
            permissions += self.get_permissions(role_id = r.id)
        return permissions
    
    def get_role_users(self, role_id, **options):
        '''
        Returns all user which is assigned to specified role.
        
        @param role_id: role ID
        
        @return: [user as DynamicObject]
        '''
        
        raise NotImplementedError()

    def get_permission_roles(self, permission_id, **options):
        '''
        Returns all roles which are including specified permission.
        
        @param permission_id: permission ID
        
        @return: [role as DynamicObject]
        '''

        raise NotImplementedError()
