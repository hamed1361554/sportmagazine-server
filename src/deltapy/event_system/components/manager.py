'''
Created on Apr 7, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.event_system.manager import DeltaEventManager
from deltapy.event_system import EVENT_MANAGER
from deltapy.application.decorators import register

@register(EVENT_MANAGER)
class EventManagerManagerComponent(DeltaEventManager):
    '''
    
    '''