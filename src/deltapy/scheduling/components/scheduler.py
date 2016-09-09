'''
Created on Jan 24, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.scheduling.manager import Scheduler
from deltapy.application.decorators import register
from deltapy.locals import APP_SCHEDULING

@register(APP_SCHEDULING)
class SchedulerComponent(Scheduler):
    '''
    
    '''