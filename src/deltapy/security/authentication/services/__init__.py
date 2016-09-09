'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security.authentication import APP_AUTHENTICATOR
from deltapy.event_system.decorators import delta_event

@delta_event('security.authentication.internal_login')
def internal_login(user_name, **options):
    '''
    Logins internally and returns security ticket
    
    @param user_name: user name
    @param **options:  
    
    @return: object
    '''
    
    return get_component(APP_AUTHENTICATOR).internal_login(user_name, **options)

@delta_event('security.authentication.login')
def login(user_name, password, **options):
    '''
    Logins and returns security ticket
    
    @param user_name: user name
    @param password: user password
    @param **options:  
    
    @return: object
    '''

    return get_component(APP_AUTHENTICATOR).login(user_name, password, **options)

def authenticate(ticket, user_name, **options):
    '''
    Authenticates user and ticket.
    
    @param ticket: security ticket
    @param user_name: user name
    @param **options: 
    
    @return: Session
    '''
    
    return get_component(APP_AUTHENTICATOR).authenticate(ticket, user_name, **options)

@delta_event('security.authentication.logout')
def logout(ticket, user_name, **options):
    '''
    Logs off given user.
    
    @param ticket: ticket
    @param user_name: user name
    @param **options: 
    '''
    
    return get_component(APP_AUTHENTICATOR).logout(ticket, user_name, **options)

def get_trusted_ips():
    '''
    Returns a list of IPs that can be trusted.
    
    @return: List of trusted IPs.
    @rtype: list(str)
    '''
    return get_component(APP_AUTHENTICATOR).get_trusted_ips()
