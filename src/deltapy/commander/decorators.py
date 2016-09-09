'''
Created on Aug 14, 2009

@author: majid v.a, abi m.s
'''

import time

import deltapy.logging.services as logging
from deltapy.commander.command import Command
import deltapy.commander.services as commander
from deltapy.event_system.decorators import delta_event

def command(key, **options):
    """
    Perform checking the user permission on this transaction before executing the decorated function.

    Example
        @command('create_customer')
        def func(...):
            ...
    """

    def command_decorator(f):
        """
        The decorator function.
        """

        def new_func(*args, **kwds):
            """
            The function that creates a new command.
            """
            # Executing the main function.
            return f(*args, **kwds)

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__= f.__doc__
        new_func.location = f.__module__
        
        command_decorator.__name__ = f.__name__
        command_decorator.__module__ = f.__module__

        commander.add_command(Command(key, new_func, **options), **options)

        return new_func

    return command_decorator
