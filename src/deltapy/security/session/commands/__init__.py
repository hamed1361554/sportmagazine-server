'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.security.session.services as session_services

@command('session.kill')
def kill_session(session_id):
    '''
    Kills the session.
    
    @param session_id: session ID
    '''

    return session_services.kill_session(session_id)

@command('session.actives')
def get_active_sessions():
    '''
    Returns all active sessions
    
    @return: [Session]
    '''

    return session_services.get_active_sessions()

@command('session.all')
def get_sessions(**options):
    '''
    Returns all sessions
    
    @param **options:
        state: session state
            "Active": active session
            "Inactive": inactive session
            "Closed": closed session
            "Killed": killed session
            "Expired": expired session
            "Disabled": disabled session
        id: session ID
        user_id: user ID
        
    @return: [Session]
    '''
    
    return session_services.get_sessions(**options)
