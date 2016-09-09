'''
Created on Oct 17, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.security.authorization.services as authorization_services 
import deltapy.security.session.services as session_services 
from deltapy.security.authorization.authorizer import AuthorizationException

def permission(permissions):
    """
        Checks if the current user has this permissions or not.

        Example
            @permission([p1, p2, ...])
            def func(...):
                ...
    """
    
    if not isinstance(permissions, (list, tuple, set)):
        permissions = [permissions]
        
    def permission_decorator(f):
        """
            The decorate function.
        """

        def new_func(*args, **kwds):
            """
                The function that creates a new command.
            """
            
            user = session_services.get_current_user()
            if user is not None:
                authorization_services.authorize(user.id, set(permissions))
            
            # If user has permission on the transaction we execute the main function
            return f(*args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__

        permission_decorator.__name__ = f.__name__
        permission_decorator.__module__ = f.__module__

        return new_func

    return permission_decorator

def superuser(f):
    """
        Checks if the current user is super user or not.   

        Example
            @permission([p1, p2, ...])
            def func(...):
                ...
    """
    
    def new_func(*args, **kwds):
        """
            The function that creates a new command.
        """
        
        user = session_services.get_current_user()
        if user is not None:
            if not user.is_superuser:
                raise AuthorizationException('You are not super user.')
        
        # If user has permission on the transaction we execute the main function
        return f(*args, **kwds)

    # Setting the new_function name...
    new_func.__name__ = f.__name__
    new_func.__module__ = f.__module__

    superuser.__name__ = f.__name__
    superuser.__module__ = f.__module__

    return new_func
