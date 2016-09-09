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
Created on Aug 12, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DynamicObject
from deltapy.security.database.manager import SecurityManager

class NullSecurityManager(SecurityManager):
    '''
    '''
    
    def create_user(self, id, password, fullname, **options):
        '''
        Creates a new user.
        
        @param id: user ID
        @param password: password
        @param fullname: full name
        @param **options: 
        '''

        return DynamicObject(id = id, password = password, name = id, fullname = fullname)

    def is_active(self, user_id):
        '''
        Returns True if user is active.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        return True
    
    def is_expired(self, user_id):
        '''
        Returns True if user is expired.
        
        @param user_id: user ID
        
        @return: bool
        '''
        
        return False

    def get_user(self, id):
        '''
        Returns user information by specified name
        
        @param id: user name
        
        @return: user data as DynamicObject
        '''
        
        return self.create_user(id, None, id)

    def is_superuser(self, id):
        '''
        Returns True if specified user is supper user else returns False
        
        @param id: user name
        
        @return: bool
        '''
        
        return True

    def get_users(self, **options):
        '''
        Returns users using given options.
        
        @return: [DynamicObject<user info...>]
        '''
        
        return []
    