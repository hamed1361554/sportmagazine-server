'''
Created on Nov 7, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.batch.manager import BatchProcessManager
from deltapy.application.decorators import register
from deltapy.locals import APP_BATCH

@register(APP_BATCH)
class BatchProcessManagerComponent(BatchProcessManager):
    '''
    Batch process manager component.
    Only for registering in application context.
    '''