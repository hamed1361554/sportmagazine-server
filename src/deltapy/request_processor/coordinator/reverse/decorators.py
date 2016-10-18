'''
Created on May 25, 2015

@author: Hamed
'''

from deltapy.request_processor.coordinator.reverse.reverser import Reverser
import deltapy.request_processor.coordinator.reverse.services as coordinator_reverse_services


def reverse(key, **options):
    '''
    Reverser Decorator Generator
    '''

    def reverse_decorator(f):
        '''
        The decorator function.
        '''

        def new_func(*args, **kwds):
            """
            The function that creates a new reverser.
            """

            # Executing the main function.
            return f(*args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__= f.__doc__
        new_func.location = f.__module__

        reverse_decorator.__name__ = f.__name__
        reverse_decorator.__module__ = f.__module__

        coordinator_reverse_services.register_reverser(Reverser(key, new_func), **options)

        return new_func

    return reverse_decorator