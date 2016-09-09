'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator
from deltapy.request_processor.coordinator import APP_TRANSACTION_COORDINATOR
from deltapy.application.decorators import register

@register(APP_TRANSACTION_COORDINATOR)
class TransactionCoordinatorComponent(TransactionCoordinator):
    pass