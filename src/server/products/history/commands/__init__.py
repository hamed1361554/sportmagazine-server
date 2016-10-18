"""
Created on Oct 18, 2016

@author: Hamed Zekri
"""

from deltapy.commander.decorators import command
import server.products.history.services as history_services


@command('server.products.history.get')
def get(product_history_id):
    """
    Returns product history info.

    :param product_history_id:
    :return:
    """

    return history_services.get(product_history_id)


@command('server.products.history.find')
def find(**options):
    """
    Searches product histories.

    :param optiosn:
    :return:
    """

    return history_services.find(**options)


@command('server.products.history.write')
def write_history(product, colors, sizes, **options):
    """
    Writes product history.

    :param product:
    :param colors:
    :param sizes:
    :param options:
    :return:
    """

    return history_services.write_history(product, colors, sizes, **options)