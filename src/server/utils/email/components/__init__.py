"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register

from server.utils.email import SMTP_EMAIL_MANAGER
from server.utils.email.smtp_manager import SmtpEmailManager


@register(SMTP_EMAIL_MANAGER)
class SmtpEmailManagerComponent(SmtpEmailManager):
    '''
    Smtp Email Manager Component
    '''