'''
Created on Aug 14, 2009

@author: Abi.mohammadi , Majid.Vesal
'''

from deltapy.locals import get_app_context, APP_COMMANDER
import deltapy.application.services as application

def execute(key, *args, **kargs):
    '''
    Executes a command by given key.
    
    @param key: command key or command name
    @return: object
    '''
    print '!'*25, key
    return get_app_context()[APP_COMMANDER].execute(key, *args, **kargs)

def bulk_execute(commands, **options):
    '''
    Executes a command by given key.
    
    @param commands: command data list as dict<command_key, args, kwargs>:
        command_key: command key
        args: command arguments
        kwargs: command keyword arguments
    @param **options: 
    @return: object
    '''
    
    return get_app_context()[APP_COMMANDER].bulk_execute(commands, **options)

def select(fields, command_key, *args, **kwargs): 
    '''
    Executes a command and returns requested fields. 
    
    @param fields: list of requested fields 
    @param command_key: command key
    @param *args:
    @param **kwargs:
    
    @return: [DynamicObject<fields>]  
    '''
    
    return get_app_context()[APP_COMMANDER].select(fields, command_key, *args, **kwargs)

def execute_async(key, callback, *args, **kargs):
    '''
    Executes a command by given key.
    
    @param key: command key or command name
    @param callback: callback function
    @return: None 
    '''
    return get_app_context()[APP_COMMANDER].execute_async(key, 
                                                          callback, 
                                                          *args, 
                                                          **kargs)

def add_command(command, **options):
    '''
    Adds a command.
    
    @param command: command instance
    '''
    
    return get_app_context()[APP_COMMANDER].add_command(command, 
                                                        **options)

def get_commands(parent=None,
                 name_filter=None,
                 description_filter=None):
    '''
    Returns all commands.
    If any filter specified, it filter those commands.
    
    @keyword str parent: only return commands that their parrents
        matches this string.
    @keyword str name_filter: only return commands that their names
        contain this string.
    @keyword str description_filter: only return commands that their
        description contain this string.
    
    @return: list<Command>
    '''
    return get_app_context()[APP_COMMANDER].get_commands(parent=parent,
                                                         name_filter=name_filter,
                                                         description_filter=description_filter)    

def get_command(key):
    '''
    Returns the command by the given key.
    
    @param key: command key
    @return: command
    '''
    return get_app_context()[APP_COMMANDER].get_command(key)

def remove_command(command):
    '''
    Removes the given command.
    
    @param command:
    '''
    return get_app_context()[APP_COMMANDER].remove_command(command)

def remove_commands(parent):
    '''
    Removes all commands in the given parent domain.
    
    @param parent: parent name
    '''
    return get_app_context()[APP_COMMANDER].remove_commands(parent)

def set_executor(executor):
    '''
    Registers a executor by the given name
    
    @param executor: executor instance
    '''
    return get_app_context()[APP_COMMANDER].set_executor(executor)

def add_hook(hook):
    '''
    Adds a execution hook to the commander.
    
    @param hook:
    '''
    return get_app_context()[APP_COMMANDER].add_hook(hook)
    
def get_hooks():
    '''
    Returns all execution hooks.
    
    @return: list<CommandExecutionHook>
    '''
    return get_app_context()[APP_COMMANDER].get_hooks()

def get_executer():
    '''
    Returns defult executor.
    '''
    return get_app_context()[APP_COMMANDER].get_executer()
