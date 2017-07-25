"""
Created on Oct 16, 2016

@author: Hamed Zekri
"""

from deltapy.application.services import get_component
from server.purchases import SERVER_PURCHASES_MANAGER


def get(purchase_id):
    '''
    Returns purchase info.

    :param purchase_id:
    :return:
    '''

    return get_component(SERVER_PURCHASES_MANAGER).get(purchase_id)


def find(**options):
    '''
    Searches purchases.

    :param options:
    :return:
    '''

    return get_component(SERVER_PURCHASES_MANAGER).find(**options)