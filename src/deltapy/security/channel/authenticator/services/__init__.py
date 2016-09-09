'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security.channel.authenticator import APP_SECURITY_CHANNEL_AUTHENTICATOR

def authenticate(ticket, certificate, **options):
    '''
    Authenticates a certificate considering the given ticket.
    
    @param ticket: ticket
    @param certificate: certificate
    '''

    return get_component(APP_SECURITY_CHANNEL_AUTHENTICATOR).authenticate(ticket, certificate, **options)