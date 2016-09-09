"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register
from deltapy.locals import APP_SECURITY
from deltapy.security.authentication import APP_AUTHENTICATOR

from server.security.authenticator import Authenticator
from server.security.manager import SecurityManager


@register(APP_AUTHENTICATOR)
class AuthenticatorComponent(Authenticator):
    '''

    '''

    pass


@register(APP_SECURITY)
class SecurityManagerComponent(SecurityManager):
    '''
    
    '''

    pass