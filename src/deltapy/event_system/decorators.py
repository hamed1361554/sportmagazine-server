'''
Created on Apr 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.event_system.event_handler import DeltaFunctionEventHandler
import deltapy.event_system.services as event_services 

def delta_event(event_name):

    def event_decorator(f):
        """
            The decorator function.
        """        
        
        event_services.register_event(event_name, f)

        def new_func(*args, **kwds):
            return event_services.fire(event_name, *args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__= f.__doc__
        new_func.location = f.__module__
        
        event_decorator.__name__ = f.__name__
        event_decorator.__module__ = f.__module__

        return new_func

    return event_decorator


def before_handler(event_name, handler_name):
    def event_decorator(f):
        """
            The decorator function.
        """        
               
        event_services.add_event_handler(event_name, DeltaFunctionEventHandler(handler_name, f, None))            


        def new_func(*args, **kwds):
            return f(*args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__= f.__doc__
        new_func.location = f.__module__
        
        event_decorator.__name__ = f.__name__
        event_decorator.__module__ = f.__module__

        return new_func

    return event_decorator



def after_handler(event_name, handler_name):
    def event_decorator(f):
        """
            The decorator function.
        """        
        
        event_services.add_event_handler_at(event_name, DeltaFunctionEventHandler(handler_name, None, f), 0)          

        def new_func(*args, **kwds):
            return f(*args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__= f.__doc__
        new_func.location = f.__module__
        
        event_decorator.__name__ = f.__name__
        event_decorator.__module__ = f.__module__

        return new_func

    return event_decorator


