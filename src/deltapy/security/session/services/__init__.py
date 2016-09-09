'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security.session import APP_SESSION

def add_hook(hook):
    '''
    Adds a hook.
    
    @param hook: hook object instance
    '''
    
    return get_component(APP_SESSION).add_hook(hook)

def get_hooks():
    '''
    Returns all registered hooks.
    
    @return: [SessionHook]
    '''

    return get_component(APP_SESSION).get_hooks()

def create_session(user, client_ip, **options):
    '''
    Creates a session and returns it
    '''
    
    return get_component(APP_SESSION).create_session(user, client_ip, **options)

def create_internal_session(user):
    '''
    Creates an internal session and returns it
    '''
    
    return get_component(APP_SESSION).create_internal_session(user)
    
def active_session(session):
    '''
    Activates a session.
    
    @param session: session instance
    '''
    
    return get_component(APP_SESSION).active_session(session)

def get_session(ticket, validate = True):
    '''
    Returns a session by the given ticket.
    
    @param ticket: security ticket
    @param validate: validating session(default is True)
     
    @return: Session
    '''
    
    return get_component(APP_SESSION).get_session(ticket, validate)

def kill_session(session_id):
    '''
    Kills the session.
    
    @param session_id: session ID
    '''

    return get_component(APP_SESSION).kill_session(session_id)

def close_session(session):
    '''
    Closes the session.
    
    @param session: session instance
    '''

    return get_component(APP_SESSION).close_session(session)
    
def cleanup_session(session):
    '''
    Cleanups the session.
    
    @param session: session
    '''

    return get_component(APP_SESSION).cleanup_session(session)
    
def get_current_session():
    '''
    Returns current session.
    
    @return: Session
    '''
    
    return get_component(APP_SESSION).get_current_session()

def update_session(session):
    '''
    Updates session.
    
    @param session: session instance
    '''
    
    return get_component(APP_SESSION).update_session(session)

def get_active_sessions():
    '''
    Returns all active sessions
    
    @return: [Session]
    '''

    return get_component(APP_SESSION).get_active_sessions()

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
    
    return get_component(APP_SESSION).get_sessions(**options)

def get_sessions_count():
    '''
    Returns count of all sessions.
    
    @return: int
    '''
    return get_component(APP_SESSION).get_sessions_count()

def get_current_user():
    '''
    Returns current user.
    
    @return: User
    '''
    
    return get_component(APP_SESSION).get_current_user()

def check_expiration(session):
    """
    Checks if current session is expire or not.
    """

    return get_component(APP_SESSION).check_expiration(session)
