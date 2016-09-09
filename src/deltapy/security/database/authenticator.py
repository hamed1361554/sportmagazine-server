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
Created on Sep 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.authentication.authenticator import BaseAuthenticator

import deltapy.security.services as security_services 

class Authenticator(BaseAuthenticator):
    '''
    Authenticator class.
    '''
    
    def _check_password_(self, password, user, **options):        
        '''
        Checks user password validity.
        
        @param password: password
        @param user: user information
        @param **options:
        '''
        
        # Making hashed password
        hashed_password = security_services.encrypt_password(user.id, password)
        return hashed_password == user.password