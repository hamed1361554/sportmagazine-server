'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.application.decorators import register
from deltapy.security.authentication.authenticator import BaseAuthenticator
from deltapy.security.authentication import APP_AUTHENTICATOR

@register(APP_AUTHENTICATOR)
class AuthenticatorComponent(BaseAuthenticator):
    '''
    '''
    
