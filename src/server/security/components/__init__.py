"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.locals import APP_SECURITY
from deltapy.application.decorators import register
from deltapy.security.authentication import APP_AUTHENTICATOR

from server.security.manager import SecurityManager
from server.security.authenticator import Authenticator


@register(APP_AUTHENTICATOR)
class AuthenticatorComponent(Authenticator):
    '''
    Authenticator Component
    '''


@register(APP_SECURITY)
class SecurityManagerComponent(SecurityManager):
    '''
    Security Manager Component
    '''
