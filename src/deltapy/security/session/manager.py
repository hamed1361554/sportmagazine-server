'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import threading

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.security.session.session import Session
from deltapy.security.session.internal_session import InternalSession
from deltapy.security.session.id_generator import SessionIDGenerator

import deltapy.security.session.bootstrap
import deltapy.unique_id.services as unique_id_services


class SessionManagerException(DeltaException):
    '''
    '''

class InvalidSessionException(DeltaException):
    '''
    '''

class SessionNotFoundException(DeltaException):
    '''
    '''

class SessionExpirationException(DeltaException):
    '''
    '''

class SessionManager(DeltaObject):
    """
    A class for manipulating sessions.
    """

    def __init__(self):
        DeltaObject.__init__(self)
        self._sessions = {}
        self._session_lock = threading.Lock()
        self._hooks = []
        unique_id_services.register_generator('session_id', SessionIDGenerator())
        deltapy.security.session.bootstrap.boot()
        
    def _set_session_state_(self, session, state):
        '''
        Changes session state.
        
        @param session: session
        @param state: state
        '''
        
        session.set_state(state)
        
    def _release_(self, session):
        '''
        Releases the given session.
        
        @param session: session instance
        '''
        try:
            self._session_lock.acquire()
            self._sessions.pop(session.get_ticket())
        finally:
            self._session_lock.release()
            
    def _get_session_by_id_(self, session_id):
        '''
        Returns session by the given ID.
        
        @param session_id: session ID
        @return: Session
        '''
        
        for session in self._sessions.values():
            if session.get_id() == session_id:
                return session
            
        raise SessionNotFoundException('Session[id = %d] not found.' % session_id)

    def _session_to_dynamic_object(self, session):
        '''
        @param session:
        '''
        
        return DynamicObject(id = session.get_id(),
                             state = session.get_state(),
                             creation_date = session.get_creation_date(),
                             user_id = session.get_user_id(),
                             client_ip = session.get_client_ip()) 

    def add_hook(self, hook):
        '''
        Adds a hook.
        
        @param hook: hook object instance
        '''
        self._hooks.append(hook)

    def get_hooks(self):
        '''
        Returns all registered hooks.
        
        @return: [SessionHook]
        '''
        return self._hooks
    
    def create_session(self, user, client_ip, **options):
        '''
        Creates a session and returns it
        '''

        ticket = options.get('ticket')
        if ticket is None:
            ticket = unique_id_services.get_id('session_id')
        session = Session(ticket,
                          user,
                          client_ip,
                          options.get('lifetime'))
        self._sessions[session.get_ticket()] = session
        for hook in self.get_hooks():
            hook.create(session)
        return session
    
    def create_internal_session(self, user):
        '''
        Creates an internal session and returns it
        '''
        
        ticket = unique_id_services.get_id('session_id')
        session = InternalSession(ticket, user)
        self._sessions[session.get_ticket()] = session
        for hook in self.get_hooks():
            hook.create(session)
        return session 

    def active_session(self, session):
        '''
        Activates a session.
        
        @param session: session instance
        '''
        
        for hook in self.get_hooks():
            hook.active(session)        

        current_thread = threading.currentThread()
        current_thread.session = session

        #self._set_session_state_(session, Session.StateEnum.ACTIVE)
    
    def get_session(self, ticket, validate = True):
        '''
        Returns a session by the given ticket.
        
        @param ticket: security ticket
        @return: Session
        '''
        try:
            session = self._sessions[ticket]
        except KeyError:
            raise InvalidSessionException('Invalid session.')

        if validate:
            if session.get_state() not in (Session.StateEnum.INACTIVE, Session.StateEnum.ACTIVE):
                raise InvalidSessionException('Session is [%s].' % session.get_state())
        return session

    def kill_session(self, session_id):
        '''
        Kills the session.
        
        @param session_id: session ID
        '''

        session = self._get_session_by_id_(session_id)
        for hook in self.get_hooks():
            hook.kill(session)
        self._set_session_state_(session, Session.StateEnum.KILLED)
    
    def close_session(self, session):
        '''
        Closes the session.
        
        @param session: session instance
        '''

        for hook in self.get_hooks():
            hook.close(session)
        session.cleanup()
        self._set_session_state_(session, Session.StateEnum.CLOSED)
        self._release_(session)
        
    def cleanup_session(self, session):
        '''
        Cleanups the session.
        
        @param session: session
        '''

        for hook in self.get_hooks():
            hook.cleanup(session)

        #self._set_session_state_(session, Session.StateEnum.INACTIVE)

        current_thread = threading.currentThread()
        current_thread.session = None
        
    def get_current_session(self):
        '''
        Returns current session.
        
        @return: Session
        '''
        
        current_thread = threading.currentThread()
        if hasattr(current_thread, 'session') and current_thread.session is not None:
            session = current_thread.session
            if session.get_state() not in (Session.StateEnum.ACTIVE, Session.StateEnum.INACTIVE):
                raise InvalidSessionException('Session is [%s].' % session.get_state())
            return session 
        return None

    def update_session(self, session):
        '''
        Updates session.
        
        @param session: session instance
        '''
        
        self._sessions[session.get_ticket()] = session 
    
    def get_active_sessions(self):
        '''
        Returns all active sessions
        
        @return: [Session]
        '''
  
        return self.get_sessions(state = Session.StateEnum.ACTIVE)
    
    def get_sessions(self, **options):
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
        
        sessions = self._sessions.values()
        state = options.pop('state', None)
        id = options.pop('id', None)
        user_id = options.pop('user_id', None)
        
        results = []
        for session in sessions:
            if state is not None and session.get_state() != state:
                continue
            if user_id is not None and session.get_user_id() != user_id:
                continue
            if id is not None and session.get_id() != id:
                continue
            context = session.get_context()
            
            found = True
            for key, value in options.items():
                if key in context:
                    if value != context[key]:
                        found = False
                        break
            if found:
                results.append(self._session_to_dynamic_object(session))
        
        return results
    
    def get_sessions_count(self):
        '''
        Returns count of all sessions.
        
        @return: int
        '''
        return len(self._sessions)
    
    def get_current_user(self):
        '''
        Returns current user.
        
        @return: User
        '''
        
        session = self.get_current_session()
        if session is not None:
            return session.get_user()
        return None

    def __str__(self):
        return "%s{sessions:%d}" % (self.__class__.__name__, len(self._sessions))
    
    def __repr__(self):
        return str(self)

    def check_expiration(self, session):
        """
        Checks if current session is expire or not.
        """

        if session.is_expired():
            raise SessionExpirationException("The session is expired.")