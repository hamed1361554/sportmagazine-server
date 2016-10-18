'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.request_processor.coordinator.reverse import APP_REVERSE_MANAGER
from deltapy.request_processor.coordinator.reverse.manager import ReverseManager

@register(APP_REVERSE_MANAGER)
class ReverseManagerComponent(ReverseManager):
    '''
    Reverse Manager Component
    '''