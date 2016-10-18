"""
Created on Oct 18, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register

from server.products.history import SERVER_PRODUCTS_HISTORY_MANAGER
from server.products.history.manager import ProductsHistoryManager


@register(SERVER_PRODUCTS_HISTORY_MANAGER)
class ProductsHistoryManagerComponent(ProductsHistoryManager):
    """
    Products History Manager Component
    """