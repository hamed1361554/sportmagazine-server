'''
Created on Feb 2, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.security.channel.authorizer.services as services

@command('security.channel.authorizer.allowed')
def get_channel_authorized_commands(channel_id):
    '''
    Returns all authorized command on the given channel.
    
    @param channel_id: channel ID
    '''
    
    return services.get_channel_authorized_commands(channel_id)

@command('security.channel.authorizer.authorize')
def authorize(channel_id, command_key, **options):
    '''
    Authorizes the given command on the specified channel.
    
    @param channel_id: channel ID
    @param command_key: command key
    '''

    return services.authorize(channel_id, command_key, **options)

@command('command.list', replace=True)
def get_command_list(parent = None): 
    '''
    Returns available commands list.
    
    @param parent: parent command
    
    @rtype: [str]
    @return: command list
    '''

    return services.get_command_list(parent)

@command('command.doc', replace=True)
def get_command_doc(key):
    '''
    Returns defined document for the specified command. 
    
    @param key: command key
    
    @rtype: str
    @return: command document
    '''
    
    return services.get_command_doc(key)
