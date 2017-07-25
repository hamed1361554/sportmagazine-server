"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register

from server.purchases import SERVER_PURCHASES_MANAGER
from server.purchases.manager import PurchasesManager


@register(SERVER_PURCHASES_MANAGER)
class PurchasesManagerComponent(PurchasesManager):
    '''
    Purchases Manager Component
    '''