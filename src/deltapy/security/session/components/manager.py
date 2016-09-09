'''
Created on May 19, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.session.manager import SessionManager
from deltapy.application.decorators import register
from deltapy.security.session import APP_SESSION

@register(APP_SESSION)
class SessionManagerComponent(SessionManager):
    '''
    '''