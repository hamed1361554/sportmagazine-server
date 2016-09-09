'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.transaction.manager import ThreadTransactionManager
from deltapy.application.decorators import register
from deltapy.locals import APP_TRANSACTION, APP_DATABASE
from deltapy.application.services import get_component

@register(APP_TRANSACTION, get_component(APP_DATABASE))
class ThreadTransactionManagerComponent(ThreadTransactionManager):
    '''
    Just for integration with deltapy
    '''
    
