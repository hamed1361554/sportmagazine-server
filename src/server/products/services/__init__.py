"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

from deltapy.application.services import get_component

from server.products import SERVER_PRODUCTS_MANAGER


def get(product_id, **options):
    """
    Returns product info.

    :param product_id:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).get(product_id, **options)


def get_by_name(name, category, **options):
    """
    Returns product info.

    :param category:
    :param name:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).get_by_name(name, category, **options)


def create(name, price, category, colors, sizes, brands, **options):
    """
    Creates product.

    :param name:
    :param price:
    :param category:
    :param colors:
    :param sizes:
    :param brands:
    :param options:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).create(name, price, category, colors, sizes, brands, **options)


def update(id, **options):
    """
    Updates product.

    :param id:
    :param options:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).update(id, **options)


def find(**options):
    """
    Searches products.

    :param optiosn:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).update(id, **options)


def decrease_product_counter(product_id, **options):
    """
    Decreases product counter.

    :param product_id:
    :return:
    """

    return get_component(SERVER_PRODUCTS_MANAGER).decrease_product_counter(product_id, **options)