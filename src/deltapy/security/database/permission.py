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
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.permission import BasePermission
import deltapy.security.services as security_services 

class Permission(BasePermission):
    '''
    '''
    
    def __init__(self, id, name):
        '''
        Creates an instance of Permission.
        
        @param id: permission ID
        @param name: permission name
        '''
        
        self._id = id
        self._name = name

        BasePermission.__init__(self)
        
    def update(self):
        '''
        Updates the permission.
        '''
        
        security_services.add_or_update_permission(self._id, name = self._name)
        
    def get_id(self):
        '''
        Returns permission ID
        
        @return: str
        '''
        
        return self._id
    
    def get_name(self):
        '''
        Returns permission name.
        '''
        
        return self._name
        
    def __hash__(self):
        return hash(self._id)
    
    def __str__(self):
        return self._name
    
    