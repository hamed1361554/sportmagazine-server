'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.session.session import Session
import deltapy.security.services as security_services

class InternalSession(Session):
    '''
    '''

    def __init__(self, ticket, user):
        Session.__init__(self, ticket, user, client_ip='127.0.0.1')

        self._user_id = user.id
        self._user_name = user.fullname

    def get_user(self):
        '''
        Returns the user which creates this session.
        
        @return: User
        '''
        if self._user_name is not None:
            return Session.get_user(self)
        return security_services.create_internal_user(self._user_id)
