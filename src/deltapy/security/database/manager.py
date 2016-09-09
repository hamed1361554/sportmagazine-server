# Copyright (c) 2000 - 2010 Majid Vesal <mva_vesal@yahoo.com> and
# Abi M.Sangarab <abisxir@gmail.com>
#
# This file is part of Deltapy.

# Deltapy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# Deltapy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Deltapy. If not, see <http://www.gnu.org/licenses/>.
'''
Created on May 19, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from storm.locals import And, Like

from deltapy.security.manager import BaseSecurityManager,\
    SecurityManagerException
from deltapy.transaction.services import get_current_transaction_store
from deltapy.transaction.decorators import transactional
from deltapy.security.database.model import UserEntity, RoleEntity, PermissionEntity,\
    User2RoleEntity, Role2PermissionEntity
from deltapy.core import DynamicObject
from deltapy.utils.storm_aux import entity_to_dic

class UserNotFoundException(SecurityManagerException):
    '''
    '''

class RoleNotFoundException(SecurityManagerException):
    '''
    '''

class PermissionNotFoundException(SecurityManagerException):
    '''
    '''

class SecurityManager(BaseSecurityManager):
    '''
    Provides security functionality.
    '''
    
    @transactional
    def create_user(self, id, password, fullname, **options):
        '''
        Creates a new user.
        
        @param id: user ID
        @param password: password
        @param fullname: full name
        @param **options: 
        
        '''
        
        store = get_current_transaction_store()
        entity = UserEntity()
        entity.id = unicode(id)
        entity.fullname = unicode(fullname)
        entity.password = unicode(self.encrypt_password(id, password))
        store.add(entity)
        store.flush()

    @transactional
    def remove_user(self, id):
        '''
        Removes the given user.
        
        @param id: user name
        '''
        
        store = get_current_transaction_store()
        entity = store.get(UserEntity, unicode(id))
        if entity is None:
            message = _('User [{user_id}] not found.')
            raise UserNotFoundException(message.format(user_id = id))
        store.remove(entity)
        store.flush()

    @transactional
    def update_user(self, id, **params):
        '''
        Updates specified user with given parameters.
        
        @param id: user name
        @param **options: 
        '''

        store = get_current_transaction_store()
        entity = store.get(UserEntity, unicode(id))
        if entity is None:
            message = _('User [{user_id}] not found.')
            raise UserNotFoundException(message.format(user_id = id))
        entity.fullname = unicode(params.get('fullname', entity.fullname))
        password = params.get('password')
        if password is not None:
            entity.password = unicode(self.encrypt_password(id, password))
        store.flush()

    @transactional
    def get_user(self, id):
        '''
        Returns user information by specified name
        
        @param id: user name
        
        @return: user data as DynamicObject
        '''
        
        store = get_current_transaction_store()
        entity = store.get(UserEntity, unicode(id))
        if entity is None:
            message = 'User [{user_id}] not found.'
            raise UserNotFoundException(message.format(user_id = id))
        return DynamicObject(entity_to_dic(entity))

    def get_users(self, **options):
        '''
        Returns users using given options.
        
        @param **options: 
            id: user ID
            fullname: user full name
            is_active: user activation flag
            is_superuser: supper user determination flag
        
        @return: [DynamicObject<user info...>]
        '''
        
        store = get_current_transaction_store()
        expressions = []
        
        id = options.get('id')
        if id is not None:
            expressions.append([And(UserEntity, UserEntity.id == int(id))])
            
        fullname = options.get('fullname')
        if fullname is not None:
            expressions.append([Like(UserEntity, UserEntity.fullname, fullname)])

        is_active = options.get('is_active')
        if is_active is not None:
            expressions.append([And(UserEntity, UserEntity.is_active == bool(is_active))])

        is_superuser = options.get('is_superuser')
        if is_active is not None:
            expressions.append([And(UserEntity, UserEntity.is_superuser == bool(is_superuser))])
            
        entities = store.find(UserEntity, *expressions)
        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))
        return results
    
    @transactional
    def activate_user(self, id, flag):
        '''
        Active or inactive specified user. 
        
        @param id: user ID
        @param flag: activation flag(True or False)
        '''
        
        self.update_user(id, is_active = flag)
    
    def is_superuser(self, id):
        '''
        Returns True if specified user is supper user else returns False
        
        @param id: user name
        
        @return: bool
        '''
        
        user = self.get_user(id)
        return bool(user.is_superuser)

    @transactional
    def is_active(self, user_id):
        '''
        Returns True if user is active.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        user = self.get_user(user_id)
        return bool(user.is_active)
    
    @transactional
    def is_expired(self, user_id):
        '''
        Returns True if user is expired.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        # TODO: complete is_expire method
        return False

    @transactional
    def create_role(self, id, name, **options):
        '''
        Creates a new role.
        
        @param id: role ID
        @param name: role name 
        @param **options:
        '''

        store = get_current_transaction_store()
        entity = RoleEntity()
        entity.id = unicode(id)
        entity.name = unicode(name)
        store.add(entity)
        store.flush()

    @transactional
    def add_or_update_role(self, id, **options):
        '''
        Adds or updates role.
        
        @param id: role ID
        @param **options:
        '''
        
        try:
            self.get_role(id)
            self.update_role(id, **options)
        except RoleNotFoundException:
            self.create_role(id, options.get('name'))

    @transactional
    def remove_role(self, id):
        '''
        Removes specified role.
        
        @param id: role ID
        '''
        
        store = get_current_transaction_store()
        entity = store.get(RoleEntity, unicode(id))
        if entity is None:
            message = _('Role [{role_id}] not found.')
            raise RoleNotFoundException(message.format(role_id = id))
        store.remove(entity)
        store.flush()

    @transactional
    def update_role(self, id, **params):
        '''
        Removes specified role.
        
        @param id: role ID
        @param **params: 
        '''
        
        store = get_current_transaction_store()
        entity = store.get(RoleEntity, unicode(id))
        if entity is None:
            message = _('Role [{role_id}] not found.')
            raise RoleNotFoundException(message.format(role_id = id))
        entity.role_name = unicode(params.get('role_name', entity.role_name))
        store.flush()

    def get_role(self, id):
        '''
        Returns role information by given role ID.
        
        @param role_id: role ID
        '''

        store = get_current_transaction_store()
        entity = store.get(RoleEntity, unicode(id))
        if entity is None:
            message = _('Role [{role_id}] not found.')
            raise RoleNotFoundException(message.format(role_id = id))
        return DynamicObject(entity_to_dic(entity))

    def get_roles(self, **options):
        '''
        Returns roles considering given options.
        
        @param **options:
            user_id: user ID
        
        @return: [DynamicObject<...>]
        '''

        store = get_current_transaction_store()
        
        expressions = []
        
        user_id = options.get('user_id')
        if user_id is not None:
            expressions.append([And(User2RoleEntity.user_id == unicode(user_id),
                                    User2RoleEntity.role_id == RoleEntity.id)])
        
        entities = store.find(RoleEntity, *expressions)
        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))
        return results
    
    @transactional
    def assign_role(self, user_id, role_ids):
        '''
        Assigns given roles to specified user.
        
        @param user_id: user ID
        @param role_ids: list role ID
        '''
        
        store = get_current_transaction_store()
        for role_id in role_ids:
            entity = store.find(User2RoleEntity, 
                                And(User2RoleEntity.user_id == unicode(user_id),
                                    User2RoleEntity.role_id == unicode(role_id))).one()
            if entity is None:
                u2r = User2RoleEntity()
                u2r.user_id = unicode(user_id)
                u2r.role_id = unicode(role_id)
                store.add(u2r)
        store.flush()

    @transactional
    def unassign_role(self, user_id, role_ids):
        '''
        Unassigns given roles from specified user.
        
        @param user_id: user ID
        @param role_ids: list role ID
        '''
        
        store = get_current_transaction_store()
        for role_id in role_ids:
            entity = store.find(User2RoleEntity, 
                                And(User2RoleEntity.user_id == unicode(user_id),
                                    User2RoleEntity.role_id == unicode(role_id))).one()
            if entity is not None:
                store.remove(entity)
        store.flush()

    @transactional
    def create_permission(self, id, name, **options):
        '''
        Creates a new permission.
        @param id: permission ID
        @param name: permission name
        @param **options: 
        '''
        
        store = get_current_transaction_store()
        entity = PermissionEntity()
        entity.id = unicode(id)
        entity.name = unicode(name)
        store.add(entity)
        store.flush() 
    
    @transactional
    def add_or_update_permission(self, id, **options):
        '''
        Adds new permission or updates existed permission.
        @param id: permission ID
        '''

        try:
            self.get_permission(id)
            self.update_permission(id, **options)
        except PermissionNotFoundException:
            self.create_permission(id, options.get('name'))
        

    @transactional
    def remove_permission(self, id):
        '''
        Removes specified permission.
        
        @param id: permission ID
        '''
        
        store = get_current_transaction_store()
        entity = store.get(PermissionEntity, unicode(id))
        if entity is None:
            message = _('Permission [{id}] not found.')
            raise PermissionNotFoundException(message.format(id = id))
        store.remove(entity)
        store.flush()

    @transactional
    def update_permission(self, id, **params):
        '''
        Updates specified permission using given parameters. 
        @param id: permission ID
        @param **params: 
        '''
        
        store = get_current_transaction_store()
        entity = store.get(PermissionEntity, unicode(id))
        if entity is None:
            message = _('Permission [{permission_id}] not found.')
            raise PermissionNotFoundException(message.format(permission_id = id))
        entity.name = unicode(params.get('name', entity.name))
        store.flush()

    def get_permission(self, id):
        '''
        Returns specified permission information.
        @param id:
        '''
        
        store = get_current_transaction_store()
        entity = store.get(PermissionEntity, unicode(id))
        if entity is None:
            message = _('Permission [{permission_id}] not found.')
            raise PermissionNotFoundException(message.format(permission_id = id))
        return DynamicObject(entity_to_dic(entity))
    
    def get_permissions(self, **options):
        '''
        Returns a list of permission considering given options.
        
        @param **options:
            role_id: role ID
        
        '''
        
        store = get_current_transaction_store()
        expressions = []
        
        role_id = options.get('role_id')
        if role_id is not None:
            expressions.append([And(Role2PermissionEntity.permission_id == PermissionEntity.id,
                                    Role2PermissionEntity.role_id == unicode(role_id))])
        
        entities = store.find(PermissionEntity, *expressions)
        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))
        return results
    
    @transactional
    def grant_permission(self, role_id, permission_ids):
        '''
        Grants given permissions.
        
        @param role_id: role ID
        @param permission_ids: list of permission ID
        '''
        
        store = get_current_transaction_store()
        for permission_id in permission_ids:
            entity = store.find(Role2PermissionEntity,
                                And(Role2PermissionEntity.role_id == unicode(role_id),
                                    Role2PermissionEntity.permission_id == unicode(permission_id))).one()
            if entity is None:
                r2p = Role2PermissionEntity()
                r2p.permission_id = unicode(permission_id)
                r2p.role_id = unicode(role_id)
                store.add(r2p)
        store.flush()
    
    @transactional
    def deny_permission(self, role_id, permission_ids):
        '''
        Denies given permissions.
        
        @param role_id: role ID
        @param permission_ids: list of permission ID
        '''
        
        store = get_current_transaction_store()
        for permission_id in permission_ids:
            entity = store.find(Role2PermissionEntity,
                                And(Role2PermissionEntity.role_id == unicode(role_id),
                                    Role2PermissionEntity.permission_id == unicode(permission_id))).one()
            if entity is not None:
                store.remove(entity)
        store.flush()
            
    def get_role_users(self, role_id, **options):
        '''
        Returns all user which are assigned to specified role.
        
        @param role_id: role ID
        
        @return: [user as DynamicObject]
        '''
        
        store = get_current_transaction_store()
        entities = store.find(UserEntity, And(UserEntity.id == User2RoleEntity.user_id,
                                              User2RoleEntity.role_id == unicode(role_id)))
        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))
        return results

    def get_permission_roles(self, permission_id, **options):
        '''
        Returns all roles which are including specified permission.
        
        @param permission_id: permission ID
        
        @return: [role as DynamicObject]
        '''

        store = get_current_transaction_store()
        entities = store.find(RoleEntity, And(RoleEntity.id == Role2PermissionEntity.role_id,
                                              Role2PermissionEntity.permission_id == unicode(permission_id)))
        results = []
        for entity in entities:
            results.append(DynamicObject(entity_to_dic(entity)))
        return results
