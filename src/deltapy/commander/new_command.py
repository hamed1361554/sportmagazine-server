'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaException
from deltapy.core import DeltaObject

class CommandException(DeltaException):
    pass

class Command(DeltaObject):
    '''
    Providing command basic methods.
    '''
    def __init__(self, manager, key, func, permissions = None):
        
        # Calling super class
        DeltaObject.__init__(self)
        
        self.__key = key
        self.__func = func
        self.__before_execution_funcs = []
        self.__after_execution_funcs = []
        if not manager:
            raise CommandException('Command manager is invalid.')
        self.__manager = manager
        self.__permissions = permissions or []
        self.__executor = None
        if hasattr(func,'location'):
            self.__location = func.location
        else:
            self.__location = func.__module__
            
        manager.add_command(self)
            
    def __str__(self):
        return self.__key
    
    def __repr__(self):
        return self.__key

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
    
    def get_location(self):
        return self.__location

    def get_doc(self):
        return self.__func.__doc__

    def __execute__(self, *args, **kargs):
             
        if len(self.get_before_execution_funcs()):
            for before in self.get_before_execution_funcs():
                before(*args, **kargs)
        
        result = self.__func(*args, **kargs)
        
        if len(self.get_after_execution_funcs()):
            for after in self.get_after_execution_funcs():
                after(*args, **kargs)
                
    
    def execute(self, *args, **kargs):
        '''
        Executes the target function of the command
        And returns target function execution result.
        '''
        
        if not self.__manager:
            raise CommandException("The command[%s] is not connected to command manager." % self)
        
        self.__manager.execute(self, *args, **kargs)
            

    def get_after_execution_funcs(self):
        return self.__after_execution_funcs

    def __check_permissions__(self):
        pass


    def get_key(self):
        return self.__key
    
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
