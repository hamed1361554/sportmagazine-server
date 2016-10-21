"""
Created on Oct 18, 2016

@author: Hamed Zekri
"""

from deltapy.application.services import get_component
from server.products.history import SERVER_PRODUCTS_HISTORY_MANAGER


def get(product_history_id):
    """
    Returns product history info.

    :param product_history_id:
    :return:
    """

    return get_component(SERVER_PRODUCTS_HISTORY_MANAGER).get(product_history_id)


def find(**options):
    """
    Searches product histories.

    :param optiosn:
    :return:
    """

    return get_component(SERVER_PRODUCTS_HISTORY_MANAGER).find(**options)


def write_history(product, colors, sizes, brands, **options):
    """
    Writes product history.

    :param product:
    :param colors:
    :param sizes:
    :param brands:
    :param options:
    :return:
    """

    return get_component(SERVER_PRODUCTS_HISTORY_MANAGER).write_history(product, colors, sizes, brands, **options)