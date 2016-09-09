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

from deltapy.unique_id.generators.int_uuid_generator.generator import IntUUIDGenerator
from deltapy.application.decorators import register
from deltapy.unique_id.generators.int_uuid_generator import INT_UUID_GENERATOR

import deltapy.unique_id.services as unique_id

@register(INT_UUID_GENERATOR)
class UUIDGeneratorComponent(IntUUIDGenerator):
    def __init__(self):
        IntUUIDGenerator.__init__(self)
        
        unique_id.register_generator('int_uuid', self)
