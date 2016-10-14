"""
Created on Oct 14, 2016

@author: Hamed Zekri
"""

from deltapy.security.session.services import get_current_user


def generate_product_unique_name(name, category):
    """
    Generates product unique name.
    """

    current_user_id = get_current_user().id
    return "{0}]*[{1}]*[{2}".format(name, category, current_user_id)