"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.application.services import get_component

from server.utils.email import SMTP_EMAIL_MANAGER


def send_activation_email(full_name, email, url):
    '''
    Sends activation email via smtp protocol.

    :param full_name:
    :param email:
    :param url:
    '''

    return get_component(SMTP_EMAIL_MANAGER).send_activation_email(full_name, email, url)


def send_change_password_email(full_name, email, change_code):
    '''
    Sends change password email via smtp protocol.

    :param full_name:
    :param email:
    :param change_code:
    '''

    return get_component(SMTP_EMAIL_MANAGER).send_change_password_email(full_name, email, change_code)