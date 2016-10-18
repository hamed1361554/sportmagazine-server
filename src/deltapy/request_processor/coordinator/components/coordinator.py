'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.request_processor.coordinator import APP_TRANSACTION_COORDINATOR
from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator


@register(APP_TRANSACTION_COORDINATOR)
class TransactionCoordinatorComponent(TransactionCoordinator):
    '''
    Transaction Coordinator Component
    '''