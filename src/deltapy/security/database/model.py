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
Created on Aug 3, 2009

@author: mohammadi
'''

from storm.locals import Storm, Unicode, ReferenceSet, Reference, Int, DateTime

class PermissionEntity(Storm):
    __storm_table__ = 'PERMISSIONS'
    __storm_primary__ = 'id'

    id = Unicode(name='id')
    name = Unicode(name='name')
    
class RoleEntity(Storm):
    __storm_table__ = 'ROLES'
    __storm_primary__ = 'id'

    id = Unicode(name='id')
    name = Unicode(name='name')

    permissions = ReferenceSet(id, 'Role2PermissionEntity.role_id', 'Role2PermissionEntity.permission_id', PermissionEntity.id)

class Role2PermissionEntity(Storm):
    __storm_table__ = 'ROLES2PERMISSIONS'
    __storm_primary__ = 'role_id', 'permission_id'

    role_id = Unicode(name='role_id')
    permission_id = Unicode(name='permission_id')

    role = Reference(role_id, RoleEntity.id)
    permission = Reference(permission_id, PermissionEntity.id)

class UserEntity(Storm):
    __storm_table__ = 'USERS'
    __storm_primary__ = 'id'

    id = Unicode(name='id')
    fullname = Unicode(name='fullname')
    password = Unicode(name='password')
    is_active = Int(name='is_active')
    is_superuser = Int(name='is_superuser')
    creation_date = DateTime(name='creation_date')

    roles = ReferenceSet(id, 'User2RoleEntity.user_id', 'User2RoleEntity.role_id', RoleEntity.id)

class User2RoleEntity(Storm):
    __storm_table__ = 'USERS2ROLES'
    __storm_primary__ = 'user_id', 'role_id'

    user_id = Unicode(name='user_id')
    role_id = Unicode(name='role_id')

    user = Reference(user_id, UserEntity.id)
    role = Reference(role_id, RoleEntity.id)
