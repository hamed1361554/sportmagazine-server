'''
Created on Nov 23, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.commander.services as commander 

@command('command.list')
def get_commands_list(parent = None):
    '''
    Returns all command in the given parent domain.
    
    @param parent: parent name
    @return: list<Command>
    '''

    return [command.get_name() for command in commander.get_commands(parent)]

@command('command.names')
def get_commands_names(parent = None):
    '''
    Returns all command in the given parent domain.
    
    @param parent: parent name
    @return: list<Command>
    '''

    return [command.get_name() for command in commander.get_commands(parent)]  


@command('command.doc')
def get_command_doc(key):
    """
    It returns document of given command.
    
    @param key: command key.
    @return: str 
    """
       
    cmd = commander.get_command(key)
    if cmd:
        return cmd.get_doc()
    return "command [%s] not found!"% key

@command('command.description')
def get_command_description(key):
    """
    Returns description of the given command.
    
    @param key: command key.
    @return: str 
    """
       
    cmd = commander.get_command(key)
    if cmd:
        return cmd.get_description()
    return "command [%s] not found!"% key

@command('command.find')
def find_commands(parent=None,
                  name_filter=None,
                  description_filter=None):
    '''
    Finds commands according to the specified filters.
    
    @keyword str parent: only return commands that their parrents
        matches this string.
    @keyword str name_filter: only return commands that their names
        contain this string.
    @keyword str description_filter: only return commands that their
        description contain this string.

    @return: founded commands
    @rtype: list(dict(str name,
                      str description))
    '''
    
    commands = commander.get_commands(parent=parent,
                                      name_filter=name_filter,
                                      description_filter=description_filter)
    
    return [{'name': cmd.get_name(), 'description': cmd.get_description()}
            for cmd in commands]

@command('command.bulk')
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
    
    return commander.bulk_execute(commands, **options)

@command('command.select')
def select(fields, command_key, *args, **kwargs): 
    '''
    Executes a command and returns requested fields. 
    
    @param fields: list of requested fields 
    @param command_key: command key
    @param *args:
    @param **kwargs:
    
    @return: [DynamicObject<fields>]  
    '''
    
    return commander.select(fields, command_key, *args, **kwargs)

