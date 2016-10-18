'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from threading import current_thread

import copy
import time

from deltapy.core import DeltaException, Context

import deltapy.security.services as security_services
import deltapy.security.session.services as session_services
import deltapy.unique_id.services as unique_id_services

class SessionException(DeltaException):
    '''
    A class for handling session exceptions.
    '''
    pass

#class SessionContext(Context):
#    '''
#    A class for saving some data in session domain.
#    '''
#    
#    def __init__(self, session):
#        '''
#        @param session:
#        '''
#        
#        Context.__init__(self)
#        self['__session__'] = session
#        
#    def __setitem__(self, key, value):
#        '''
#        Sets new item or updates existing item in context
#        
#        @param key:
#        @param value:
#        '''
#        
#        result = Context.__setitem__(self, key, value)
#        self['__session__'].update()
#        return result

class SessionContext(dict):
    '''
    A class for saving some data in session domain.
    '''
    
    def __init__(self, session):
        '''
        @param session:
        '''
        
        super(SessionContext, self).__init__()
        self._ticket = session.get_ticket()
        
    def __setitem__(self, key, value):
        '''
        Sets new item or updates existing item in context
        
        @param key:
        @param value:
        '''
        result = super(SessionContext, self).__setitem__(key, value)
        
        # Updating session because of this change in session context
        session_services.get_session(self._ticket, False).update()
        
        return result

class Session:
    """
    A class for storing session information.
    """

    class StateEnum:
        '''
        A class for defining session state.
        '''
        ACTIVE = "Active"
        INACTIVE = "Inactive"
        CLOSED = "Closed"
        KILLED = "Killed"
        EXPIRED = "Expired"
        DISABLED = "Disabled"

    def __init__(self, ticket=None, user=None, client_ip=None, lifetime=None):
        self._ticket = ticket
        self._state = Session.StateEnum.INACTIVE
        self._create_date = time.time()
        self._id = unique_id_services.get_id('session_id')
        self._context = SessionContext(self)
        self._user_id = user.id
        self._client_ip = client_ip
        self._client_request = None
        self._lifetime = lifetime  # millisecond
        
    def get_client_ip(self):
        '''
        Returns the user IP address.
        '''
        
        return self._client_ip
        
    def close(self):
        '''
        Closes the session.
        '''
        session_services.close_session(self)
            
    def active(self, client_request):
        '''
        Activates the session. Sets this session to current thread.
        '''
        
        self._set_client_request(client_request)
        thread = current_thread()
        thread.__LOCALE__ = client_request.context.get('__LOCALE__')
        session_services.active_session(self)
        
    def _set_client_request(self, client_request):
        '''
        Sets call context to session.
        '''
        
        if client_request.context is None:
            client_request.context = {}
        self._client_request = copy.deepcopy(client_request)
        
    def get_call_context(self):
        '''
        Returns call context.
        
        @return {}
        '''
        
        return self._client_request.context

    def get_internal_context(self):
        '''
        Retunrs internal system context for the current call

        @rtype: dict
        @return: internal context dictionary
        '''

        if not hasattr(self._client_request, 'internal_context') or \
           self._client_request.internal_context is None:
            self._client_request.internal_context = {}

        return self._client_request.internal_context
    
    def get_client_request(self):
        '''
        Returns current client request.
        
        @rtype: ClientRequest
        @return: client request
        '''
        
        return self._client_request

    def get_ticket(self):
        '''
        Returns session ID.
        
        @return: str
        '''
        
        return self._ticket
    
    def get_id(self):
        '''
        Returns session ID.
        
        @return: int
        '''
        
        return self._id
        

    def get_user(self):
        '''
        Returns the user which creates this session.
        
        @return: user
        '''
        
        return security_services.get_user(self._user_id)
    
    def get_user_id(self):
        '''
        Returns the user which creates this session.
        
        @return: user
        '''
        
        return self._user_id

    def update(self):
        '''
        Updates session.
        '''
        
        session_services.update_session(self)
        
    def cleanup(self):
        '''
        Cleanups the session.
        '''
        
        session_services.cleanup_session(self)
            
    def get_state(self):
        '''
        Returns the session state.
        
        @return: str
        '''
        
        return self._state
    
    def set_state(self, state):
        '''
        Returns the session state.
        
        @return: str
        '''
        
        self._state = state
        self.update()

    def get_creation_date(self):
        '''
        Returns the session creation date.
        
        @return: 
        '''
        
        return time.ctime(self._create_date)
    
    def get_context(self):
        '''
        Returns session context.
        
        @return: SessionContext
        '''
        
        return self._context 
    
    def __str__(self):
        return "%s[%s]" % (self.__class__.__name__, self.get_ticket())
    
    def __repr__(self):
        return "%s[%s]" % (self.__class__.__name__, self.get_ticket())

    def is_expired(self):
        """
        If session is expired, returns True.

        @return: Is expired
        @rtype: bool
        """

        if self._lifetime is not None and self._lifetime > 0:
            # 300 seconds waite is the tolerance !
            # The unit of lifetime is millisecond
            if (time.time() - self._create_date) * 1000 > self._lifetime + 300000:
                return True

        return False
