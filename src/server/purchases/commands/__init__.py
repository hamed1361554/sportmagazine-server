"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.commander.decorators import command
import server.purchases.services as purchases_services


@command('server.purchases.get')
def get(invoice_id):
    '''
    Returns invoice info.

    :param invoice_id:
    :return:
    '''

    return purchases_services.get(invoice_id)


@command('server.purchases.find')
def find(**options):
    '''
    Searches purchases.

    :param options:
    :return:
    '''

    return purchases_services.find(**options)