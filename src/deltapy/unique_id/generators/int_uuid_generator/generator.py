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
Created on Mar 4, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import uuid

from deltapy.unique_id.generator import UniqueIDGenerator

class IntUUIDGenerator(UniqueIDGenerator):
    '''
    '''
    
    def get(self, **options):
        '''
        Returns an unique ID by given options
        
        @param **options: custom parameters
        @return: object 
        '''
        
        id = 10000000000 - hash(uuid.uuid4())
        return id
    
    def refresh(self, **options):
        '''
        Refreshes the unique ID generator by given options
        
        @param **options: custom parameters
        '''
        
        pass
