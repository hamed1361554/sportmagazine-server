'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.security.authentication.services as services
from deltapy.commander.decorators import command

@command('security.authenticate')
def authenticate(ticket, user_name, **options):
    '''
    Authenticates user and ticket.
    
    @param ticket: security ticket
    @param user_name: user name
    @param **options: 
    
    @return: Session
    '''
    
    services.authenticate(ticket, user_name, **options)
