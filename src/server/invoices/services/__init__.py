"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.application.services import get_component
from server.invoices import SERVER_INVOICES_MANAGER


def get(invoice_id):
    '''
    Returns invoice info.

    :param invoice_id:
    :return:
    '''

    return get_component(SERVER_INVOICES_MANAGER).get(invoice_id)


def find(**options):
    '''
    Searches invoices.

    :param options:
    :return:
    '''

    return get_component(SERVER_INVOICES_MANAGER).find(**options)


def register(invoice_items):
    '''
    Registers new invoice.

    :param invoice_items:
    :return:
    '''

    return get_component(SERVER_INVOICES_MANAGER).register(invoice_items)


def update(invoice_id, **options):
    '''
    updates invoices.

    :param options:
    :return:
    '''

    return get_component(SERVER_INVOICES_MANAGER).update(invoice_id, **options)