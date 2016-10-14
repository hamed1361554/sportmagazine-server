"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register

from server.products import SERVER_PRODUCTS_MANAGER
from server.products.manager import ProductsManager


@register(SERVER_PRODUCTS_MANAGER)
class ProductsManagerComponent(ProductsManager):
    """
    Products Manager Component
    """