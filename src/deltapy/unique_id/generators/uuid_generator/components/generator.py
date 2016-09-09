'''
Created on Mar 4, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.unique_id.generators.uuid_generator.generator import UUIDGenerator
from deltapy.application.decorators import register
from deltapy.unique_id.generators.uuid_generator import UUID_GENERATOR

import deltapy.unique_id.services as unique_id

@register(UUID_GENERATOR)
class UUIDGeneratorComponent(UUIDGenerator):
    def __init__(self):
        UUIDGenerator.__init__(self)
        
        unique_id.register_generator('uuid', self)
