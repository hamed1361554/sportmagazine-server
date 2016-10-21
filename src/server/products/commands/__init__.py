"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

from deltapy.commander.decorators import command
import server.products.services as products_services


@command('server.products.get')
def get(product_id):
    """
    Returns product info.

    :param product_id:
    :return:
    """

    return products_services.get(product_id)


@command('server.products.get.by_name')
def get_by_name(name, category):
    """
    Returns product info.

    :param category:
    :param name:
    :return:
    """

    return products_services.get_by_name(name, category)


@command('server.products.create')
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

    return products_services.create(name, price, category, colors, sizes, brands, **options)


@command('server.products.update')
def update(id, **options):
    """
    Updates product.

    :param id:
    :param options:
    :return:
    """

    return products_services.update(id, **options)


@command('server.products.find')
def find(**options):
    """
    Searches products.

    :param optiosn:
    :return:
    """

    return products_services.update(id, **options)