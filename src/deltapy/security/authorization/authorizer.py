'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException
import deltapy.security.services as security_services
import deltapy.security.session.services as session_services

class AuthorizationException(DeltaException):
    '''
    '''
    
class BaseAuthorizer(DeltaObject):
    '''
    '''

    def authorize(self, user_id, permission_ids):
        '''
        Authorizes user for permissions.
        
        @param user_id: user ID
        @param permission_ids: list of permission ID 
        '''
        
        if not security_services.is_superuser(user_id):
            user_permissions = security_services.get_user_permissions(user_id)
            user_permission_ids = [p.id for p in user_permissions]
            
            # Checking for iterable object
            _permission_ids = permission_ids
            if not isinstance(permission_ids, (list, tuple, set)):
                _permission_ids = [permission_ids]
            
            if not set(_permission_ids) <= set(user_permission_ids):
                message = _('The user[{user_name}] has not permission(s) {permission_ids}.')
                raise AuthorizationException(message.format(user_name = user_id, 
                                                            permission_ids = permission_ids))
            
    def is_in_role(self, permission_ids, user_id=None):
        '''
        Returns True if current user has permissions.
         
        @param permission_ids: list of permission ID
        @param user_id: user_id to check it's roles 
        
        @return: bool
        '''
        
        if user_id is None:
            user_id = session_services.get_current_user().id
        
        try:
            self.authorize(user_id, permission_ids)
            return True
        except AuthorizationException:
            return False
        