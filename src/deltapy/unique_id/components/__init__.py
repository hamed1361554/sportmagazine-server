'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.unique_id.manager import UniqueIDManager
from deltapy.application.decorators import register
from deltapy.unique_id import UNIQUE_ID_MANAGER

@register(UNIQUE_ID_MANAGER)
class UniqueIDManagerComponent(UniqueIDManager):
    '''
    '''