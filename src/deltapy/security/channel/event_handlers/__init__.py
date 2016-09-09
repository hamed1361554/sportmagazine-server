'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.event_system.decorators import after_handler
import deltapy.security.channel.authenticator.services as channel_authenticator_services 

@after_handler('security.authentication.login', 'channel_after_login_handler')
def after_login_handler(params):
    
    ticket = params['result']
    options = dict(params['kwargs'])
    certificate = options.get('certificate')
    if 'certificate' in options:
        options.pop('certificate') 
    
    channel_authenticator_services.authenticate(ticket, certificate, **options)