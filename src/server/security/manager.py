"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from storm.expr import Select, And

from deltapy.core import DynamicObject
from deltapy.utils.storm_aux import entity_to_dic
from deltapy.transaction.decorators import transactional
from deltapy.security.manager import BaseSecurityManager
from deltapy.transaction.services import get_current_transaction_store

from server.model import UserEntity


class SecurityManager(BaseSecurityManager):
    """
    Security Manager
    """

    def __init__(self):
        BaseSecurityManager.__init__(self)

    def create_user(self, id, password, fullname, **options):
        """
        Creates a new user.

        @param id: user ID
        @param password: password
        @param fullname: full name
        """

        pass

    def remove_user(self, id):
        """
        Removes the given user.

        @param id: user name
        """

        pass

    def update_user(self, id, **params):
        """
        Updates specified user with given parameters.

        @param id: user name
        @param **options:
        """

        pass

    def activate_user(self, id, flag):
        """
        Active or inactive specified user.

        @param id: user ID
        @param flag: activation flag(True or False)
        """

        pass

    def is_active(self, user_id):
        """
        Returns True if user is active.

        @param user_id: user ID

        @return: bool
        """

        return True

    def is_expired(self, user_id):
        """
        Returns True if user is expired.

        @param user_id: user ID

        @return: bool
        """

        return False

    @transactional
    def get_user(self, id):
        """
        Returns user information by specified name

        @param id: user name

        @return: user data as DynamicObject
        """

        store = get_current_transaction_store()
        user = store.find(UserEntity, And(UserEntity.id == id)).one()

        return DynamicObject(entity_to_dic(user))

    @transactional
    def get_user_by_id(self, user_id):
        """
        Returns user information by specified name

        @param user_id: user ID

        @return: user data as DynamicObject
        """

        store = get_current_transaction_store()
        user = store.find(UserEntity, And(UserEntity.user_id == unicode(user_id))).one()

        return DynamicObject(entity_to_dic(user))

    def is_superuser(self, id):
        """
        Returns True if specified user is supper user else returns False

        @param id: user name

        @return: bool
        """

        return True

    def get_users(self, **options):
        """
        Returns users using given options.

        @return: [DynamicObject<user info...>]
        """

        return []

    def reset_password(self, user_id, new_password):
        """
        Resets password of the given user to new password.

        @param user_id: user ID
        @param new_password: user new password
        """

        self.update_user(user_id, password = self.encrypt_password(user_id, new_password))

    def change_password(self, user_id, current_password, new_password):
        """
        Changes password of current user.

        @param current_password: user current password
        @param new_password: user new password
        """

        self.update_user(user_id, password=self.encrypt_password(user_id, new_password))

    def create_role(self, name, **options):
        """
        Creates a new role.

        @param id: role ID
        @param name: role name
        @param **options: Other options.
        """

        raise NotImplementedError()

    def find_role(self, **options):
        """
        Finds role according to given options.

        @param **options: Filters of find.

        @return: List of DynamicObject
        """

        raise NotImplementedError()

    def add_or_update_role(self, id, **options):
        """
        Adds or updates role.

        @param id: role ID
        @param **options:
        """

        raise NotImplementedError()

    def remove_role(self, id):
        """
        Removes specified role.

        @param id: role ID
        """

        raise NotImplementedError()

    def update_role(self, id, **params):
        """
        Removes specified role.

        @param id: role ID
        @param **params:
        """

        raise NotImplementedError()

    def get_role(self, id, **options):
        """
        Returns role information by given role ID.

        @param role_id: role ID
        @param **options: Other options.
        """

        raise NotImplementedError()

    def get_roles(self, **options):
        """
        Returns roles considering given options.

        @return: [DynamicObject<...>]
        """

        raise NotImplementedError()

    def assign_role(self, user_id, role_ids):
        """
        Assigns given roles to specified user.

        @param user_id: user ID
        @param role_ids: list role ID
        """

        raise NotImplementedError()

    def unassign_role(self, user_id, role_ids):
        """
        Unassigns given roles from specified user.

        @param user_id: user ID
        @param role_ids: list role ID
        """

        raise NotImplementedError()

    def create_permission(self, id, name, **options):
        """
        Creates a new permission.
        @param id: permission ID
        @param name: permission name
        @param **options:
        """

        raise NotImplementedError()

    def add_or_update_permission(self, id, **options):
        """
        Adds new permission or updates existed permission.
        @param id: permission ID
        """

        raise NotImplementedError()

    def remove_permission(self, id):
        """
        Removes specified permission.

        @param id: permission ID
        """

        raise NotImplementedError()

    def update_permission(self, id, **params):
        """
        Updates specified permission using given parameters.
        @param id: permission ID
        @param **params:
        """

        raise NotImplementedError()

    def get_permission(self, id):
        """
        Returns specified permission information.
        @param id:
        """

        raise NotImplementedError()

    def get_permissions(self, **options):
        """
        Returns a list of permission considering given options.
        """

        raise NotImplementedError()

    def grant_permission(self, role_id, permission_ids):
        """
        Grants given permissions.

        @param role_id: role ID
        @param permission_ids: list of permission ID
        """

        raise NotImplementedError()

    def deny_permission(self, role_id, permission_ids):
        """
        Denies given permissions.

        @param role_id: role ID
        @param permission_ids: list of permission ID
        """

        raise NotImplementedError()

    def get_user_roles(self, user_id, **options):
        """
        Returns all roles which are assigned to specified user.

        @param user_id: user ID
        @param **options:

        @return: [role as DynamicObject]
        """

        return []

    def get_role_permissions(self, role_id, **options):
        """
        Returns all permissions which are granted to specified role.

        @param role_id: role ID

        @return: [permission as DynamciObject]
        """

        return []

    def get_user_permissions(self, id):
        """
        Returns all permissions of specified user.

        @param id: user ID

        @return: [permission info as DynamicObject]
        """

        permissions = []
        for r in self.get_roles(user_id = id):
            permissions += self.get_permissions(role_id=r.id)
        return permissions

    def get_role_users(self, role_id, **options):
        """
        Returns all user which is assigned to specified role.

        @param role_id: role ID

        @return: [user as DynamicObject]
        """

        return []

    def get_permission_roles(self, permission_id, **options):
        """
        Returns all roles which are including specified permission.

        @param permission_id: permission ID

        @return: [role as DynamicObject]
        """

        return []
