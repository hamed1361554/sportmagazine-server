'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.security.authorization import APP_AUTHORIZER
from deltapy.security.authorization.authorizer import BaseAuthorizer

@register(APP_AUTHORIZER)
class AuthorizerComponent(BaseAuthorizer):
    '''
    '''
    
