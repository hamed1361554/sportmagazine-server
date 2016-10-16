"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.commander.decorators import command
import server.invoices.services as invoices_services


@command('server.invoices.get')
def get(invoice_id):
    '''
    Returns invoice info.

    :param invoice_id:
    :return:
    '''

    return invoices_services.get(invoice_id)


@command('server.invoices.find')
def find(**options):
    '''
    Searches invoices.

    :param options:
    :return:
    '''

    return invoices_services.find(**options)


@command('server.invoices.register')
def register(invoice_items):
    '''
    Registers new invoice.

    :param invoice_items:
    :return:
    '''

    return invoices_services.register(invoice_items)


@command('server.invoices.update')
def update(invoice_id, **options):
    '''
    updates invoices.

    :param options:
    :return:
    '''

    return invoices_services.update(invoice_id, **options)