'''
Created on Aug 14, 2009

@author: mohammadi, vesal
'''

import traceback

import time

from deltapy.core import DeltaException, DynamicObject
from deltapy.core import DeltaObject
from deltapy.commander.executor import CommandExecutor
from deltapy.security.session.services import get_current_session
from deltapy.utils.concurrent import run_in_thread
import deltapy.logging.services as logging

class CommandManagerException(DeltaException):
    '''
    A class for handling command manager exceptions.
    '''
    pass

class CommandManager(DeltaObject):
    '''
    Manages commands.
    '''
    
    logger = logging.get_logger(name='commander')
    
    def __init__(self):
        DeltaObject.__init__(self)
        self._commands = {}
        self._executor = CommandExecutor()
        self._hooks = []
    
    def get_executer(self):
        '''
        Returns defult executor.
        '''
        
        return self._executor
        
    def set_executor(self, executor):
        '''
        Registers a executor by the given name
        
        @param executor: executor instance
        '''
        
        self._executor = executor

    def execute(self, key, *args, **kargs):
        '''
        Executes a command by given key.
        
        @param key: command key or command name
        @return: object
        '''
        if key not in self._commands:
            raise CommandManagerException("Command[%s] does not exist." % key)
        # Getting command
        command = self._commands[key]

        try:
            self._before_execute_command_(command, *args, **kargs)

            # Executing the command
            result = self._executor.execute(command, *args, **kargs)

            self._after_execute_command_(command, result, *args, **kargs)

            # Returning the command result
            return result
        except DeltaException as error:
            self._exception_(command, error, *args, **kargs)

            error_stack = traceback.format_exc()
            error_message = "[{command_key}] Error:\n{error}".format(command_key=key, error=error_stack)
            CommandManager.logger.error(error_message)
            raise
        except Exception as error:
            self._exception_(command, error, *args, **kargs)

            error_stack = traceback.format_exc()
            error_message = "[{command_key}] Error:\n{error}".format(command_key=key, error=error_stack)
            CommandManager.logger.error(error_message)

            # If it's an standard error, there is no need to wrap it again,
            # because it can be pickled with no difficulty.
            if isinstance(error, StandardError):
                raise

            raise Exception("%s:%s" % (str(error), error_stack))
    
    def bulk_execute(self, commands, **options):
        '''
        Executes a command by given key.
        
        @param commands: command data list as dict<command_key, args, kwargs>:
            command_key: command key
            args: command arguments
            kwargs: command keyword arguments
        @param **options: 
        @return: object
        '''

        if len(commands) == 0:
            raise CommandManagerException('There is no command to execute.')
        
        results = []
        for command_data in commands:
            command_key = command_data['command_key']
            args = command_data.get('args', tuple())
            if not isinstance(args, (tuple, list)):
                args = (args,)
            kwargs = command_data.get('kwargs', dict())
            result = self.execute(command_key, 
                                  *args, 
                                  **kwargs)
            results.append(DynamicObject(command_key = command_key,
                                         command_result = result))
        return results
    
    def select(self, fields, command_key, *args, **kwargs): 
        '''
        Executes a command and returns requested fields. 
        
        @param fields: list of requested fields 
        @param command_key: command key
        @param *args:
        @param **kwargs:
        
        @return: [DynamicObject<fields>]  
        '''

        result = self.execute(command_key, *args, **kwargs)
        results = result
        if not isinstance(result, list):
            results = [result]
            
        if fields is None or len(fields) == 0:
            return results
        
        selected_resultes = []
        for obj in results:
            record = DynamicObject()
            for field in fields:
                record[field] = obj.get(field)
            selected_resultes.append(record)
        return selected_resultes
        
    def __execute_async__(self, key, callback, *args, **kargs):
        result = self.execute(key, *args, **kargs)
        if callback:
            callback(key, result, *args, **kargs)
        return result
    
    def execute_async(self, key, callback, *args, **kargs):
        '''
        Executes a command by given key.
        
        @param key: command key or command name
        @param callback: callback function
        @return: None 
        '''

        return run_in_thread(self.__execute_async__(key, 
                                                    callback, 
                                                    *args, 
                                                    **kargs))

    def _before_execute_command_(self, command, *args, **kargs):
        '''
        Runs before execution method of all hooks.
        
        @param command: command
        '''

        # Setting start processing time in command manager
        current_session = get_current_session()
        internal_context = current_session.get_internal_context()
        internal_context['start_process_time'] = time.time()
        
        if len(self._hooks):
            for hook in self._hooks:
                if hook.is_enable():
                    hook.before_execute(self, command, *args, **kargs)
        
    
    def _after_execute_command_(self, command, result, *args, **kargs):
        '''
        Runs after execution method of all hooks.
        
        @param command: command
        @param result: command execution result
        '''
        
        if len(self._hooks):
            for index in xrange(len(self._hooks) - 1, -1, -1):
                hook = self._hooks[index]
                if hook.is_enable():
                    hook.after_execute(self, command, result, *args, **kargs)

    def _exception_(self, command, error, *args, **kargs):
        '''
        Runs exception method of all hooks.
        
        @param command: command
        @param error: exception instance
        '''
        
        if len(self._hooks):
            for index in xrange(len(self._hooks) - 1, -1, -1):
                hook = self._hooks[index]
                if hook.is_enable():
                    hook.exception(self, command, error, *args, **kargs)

    def add_command(self, command, **options):
        '''
        Adds a command.
        
        @param command: command instance
        '''

        replace = options.get('replace', False)
        
        if not replace and command.get_key() in self._commands:
            raise DeltaException("Command[%s] already exists." % command)
        
        command.attach(self)
        
        self._commands[command.get_key()] = command

    def get_commands(self,
                     parent=None,
                     name_filter=None,
                     description_filter=None,
                     exact_name=None):
        '''
        Returns all commands.
        If any filter specified, it filter those commands.

        @keyword str parent: only return commands that their parrents
            matches this string.
        @keyword str name_filter: only return commands that their names
            contain this string.
        @keyword str exact_name: only return command that its name
            is this string.
        @keyword str description_filter: only return commands that their
            description contain this string.

        @return: founded commands
        @rtype: list(dict(str name,
                          str description))
        '''
        commands = self._commands.values()
        results = []

        if (parent is None and name_filter is None and
            description_filter is None and exact_name is None):
            # If no filter provided.
            return commands

        for cmd in commands:
            filtered = False

            if parent is not None:
                if not cmd.get_location().startswith(parent):
                    filtered = True
            if name_filter is not None:
                if cmd.get_name().find(name_filter) < 0:
                    filtered = True
            if exact_name is not None:
                if cmd.get_name() != exact_name:
                    filtered = True
            if description_filter is not None:
                command_description = cmd.get_description()
                if (command_description is None or
                    command_description.find(description_filter) < 0):
                    filtered = True

            if not filtered:
                results.append(cmd)

        return results

    def remove_commands(self, parent):
        '''
        Removes all commands in the given parent domain.
        
        @param parent: parent name
        '''
        for cmd in self._commands.values():
            if cmd.location.find(parent) == 0:
                self.remove_command(cmd)
                        

    def get_command(self, key):
        '''
        Returns the command by the given key.
        
        @param key: command key
        @return: command
        '''
        
        if key in self._commands:
            return self._commands[key]
        return None

    def remove_command(self, command):
        '''
        Removes the given command.
        
        @param command:
        '''
        
        if command.get_key() in self._commands:
            command = self._commands.pop(command.get_key())
            command.dettach(self)
            del command
            
    def add_hook(self, hook):
        '''
        Adds an execution hook to the commander.
        
        @param hook:
        '''
        
        self._hooks.append(hook)
        
    def get_hooks(self):
        '''
        Returns all execution hooks.
        
        @return: list<CommandExecutionHook>
        '''
        
        return self._hooks

