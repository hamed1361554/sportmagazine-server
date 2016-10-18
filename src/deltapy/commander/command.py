'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaException
from deltapy.core import DeltaObject
import deltapy.security.authorization.services as authorization_services
import deltapy.security.session.services as session_services

class Command(DeltaObject):
    '''
    Providing command basic methods.
    '''
    def __init__(self, key, func, **options):
        
        # Calling super class
        DeltaObject.__init__(self)
        
        self.__key = key
        self.__func = func

        self.__before_execution_funcs = options.get('before_execution_funcs')
        if self.__before_execution_funcs is None:
            self.__before_execution_funcs = []

        self.__after_execution_funcs = options.get('after_execution_funcs')
        if self.__after_execution_funcs is None:
            self.__after_execution_funcs = []

        self.__on_execution_failed_funcs = options.get('execution_failed_funcs')
        if self.__on_execution_failed_funcs is None:
            self.__on_execution_failed_funcs = []

        self.__manager = None
        self.__description = options.get('description', None)
        permissions = options.get('permissions', None)
        self.__permissions = permissions or []
        self.__executor = None
        if hasattr(func,'location'):
            self.location = func.location
        else:
            self.location = func.__module__
        self.__options = options
            
    def __str__(self):
        return self.__key
    
    def __repr__(self):
        return self.__key
    
    def get_options(self):
        '''
        Returns command options.
        
        @return: {}
        '''
        return self.__options

    def get_option(self, name, default_value = None):
        '''
        Returns command option.
        
        @return: {}
        '''
        return self.__options.get(name, default_value)

    def set_executor(self, executor):
        '''
        Sets given executor.
        
        @param executor:
        '''
        self.__executor = executor
        
    def get_executor(self):
        '''
        Returns assigned executor.
        
        @param executor:
        '''
        return self.__executor

    def get_before_execution_funcs(self):
        '''
        Returns functions which will be executed before executing the command.
        
        @return: []
        '''
        
        return self.__before_execution_funcs

    def add_before_execution_funcs(self, func_to_execute):
        '''
        Adds func to after execution.
        '''
        self.__before_execution_funcs.add(func_to_execute)

    def get_location(self):
        '''
        Returns command location
        
        @return: str
        '''
        return self.location

    def get_doc(self):
        '''
        Returns command document.
        
        @return: str
        '''
        return self.__func.__doc__

    def get_description(self):
        '''
        Returns description of the command.

        @return: str
        '''
        return self.__description

    def execute(self, *args, **kargs):
        '''
        Executes the target function of the command
        and returns target function execution result.
        '''
        if self.__manager is None:
            raise DeltaException("The command[%s] is not connected to command manager." % self)

        self.__check_permissions()

        before_execution_funcs = self.get_before_execution_funcs()
        if before_execution_funcs is not None:
            for before_func in before_execution_funcs:
                before_func(args, kargs)

        try:
            result = self.__func(*args, **kargs)
        except Exception as error:
            execution_failed_funcs = self.get_on_execution_failed_funcs()
            if execution_failed_funcs is not None:
                for failed_func in execution_failed_funcs:
                    failed_func(args, kargs, error)

            raise

        # If there wasn't any exception.
        after_execution_funcs = self.get_after_execution_funcs()
        if after_execution_funcs is not None:
            for after_func in after_execution_funcs:
                after_func(result, args, kargs)

        return result

    def get_after_execution_funcs(self):
        '''
        Returns functions which will be executed after executing the command.
        
        @return: []
        '''
        return self.__after_execution_funcs

    def add_after_execution_funcs(self, func_to_execute):
        '''
        Adds func to after execution.
        '''

        self.__after_execution_funcs.append(func_to_execute)

    def get_on_execution_failed_funcs(self):
        '''
        Returns functions which will be executed if execution failed.
        
        @return: []
        '''
        return self.__on_execution_failed_funcs

    def add_on_execution_failed_funcs(self, func_to_execute):
        '''
        Adds func to on execution failed.
        '''

        self.__on_execution_failed_funcs.append(func_to_execute)

    def __check_permissions(self):
        if len(self.__permissions) != 0:
            user = session_services.get_current_user()
            authorization_services.authorize(user.id, self.__permissions)

    def attach(self, manager):
        self.__manager = manager

    def dettach(self, manager):
        self.__manager = None

    def get_key(self):
        return self.__key
    
    def get_name(self):
        return self.get_key()
    
class CommandGroup(Command):
    '''
    Command group. 
    '''

    def __init__(self, key):
        Command.__init__(self, key, None)
        self._commands = []
        
    def add_command(self, cmd_key, *args, **kwargs):
        '''
        Adds a command to command group.
        
        @param cmd_key: command key
        '''
        self._commands.append((cmd_key, args, kwargs))
        
    def get_commands(self):
        '''
        Returns all commands in the group.
        
        @return: list<str>
        '''
        
        return self._commands

    def execute(self, *args, **kargs):
        '''
        Executes the target function of the command
        And returns target function execution result.
        '''
        results = []
        if self.__manager:
            
            for cmd_data in self._commands:
                cmd_key, cmd_args, cmd_kargs, = cmd_data
                result = self.__manager.execute(cmd_key, cmd_args, cmd_kargs)
                results.append(result)
            return results
        else:
            raise DeltaException("The command[%s] is not connected to command manager." % self)

class ParallelCommandGroup(Command):
    '''
    Parallel command group. 
    '''

    def __init__(self, key):
        Command.__init__(self, key, None)
        self._commands = []

    def add_command(self, command_key, callback, *args, **kwargs):
        '''
        Adds a command to the command group.
        
        @param command_key: command key
        @param callback: callback function
        '''
        self._commands.append((command_key, callback, args, kwargs))

    def execute(self, *args, **kargs):    
        '''
        Executes the target function of the command
        And returns target function execution result.
        '''
        threads = []
        if self.__manager:
            
            for cmd_data in self._commands:
                cmd_key, callback, cmd_args, cmd_kargs, = cmd_data
                thread = self.__manager.execute_async(cmd_key, 
                                                      callback, 
                                                      cmd_args, 
                                                      cmd_kargs)
                threads.append(thread)
            
            for thread in threads:
                thread.join() 
            return None
        else:
            raise DeltaException("The command[%s] is not connected to command manager." % self)
