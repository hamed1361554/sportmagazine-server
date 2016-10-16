"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register

from server.invoices import SERVER_INVOICES_MANAGER
from server.invoices.manager import InvoicesManager


@register(SERVER_INVOICES_MANAGER)
class InvoicesManagerComponent(InvoicesManager):
    '''
    Invoices Manager Component
    '''