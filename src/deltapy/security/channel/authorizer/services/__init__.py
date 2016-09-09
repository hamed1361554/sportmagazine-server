'''
Created on Feb 2, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security.channel.authorizer import APP_CHANNEL_AUTHORIZER

def get_channel_authorized_commands(channel_id):
    '''
    Returns all authorized command on the given channel.
    
    @param channel_id: channel ID
    '''
    
    return get_component(APP_CHANNEL_AUTHORIZER).get_channel_authorized_commands(channel_id)

def authorize(channel_id, command_key, **options):
    '''
    Authorizes the given command on the specified channel.
    
    @param channel_id: channel ID
    @param command_key: command key
    '''

    return get_component(APP_CHANNEL_AUTHORIZER).authorize(channel_id, command_key, **options)

def get_command_list(parent = None): 
    '''
    Returns available commands list.
    
    @param parent: parent command
    
    @rtype: [str]
    @return: command list
    '''

    return get_component(APP_CHANNEL_AUTHORIZER).get_command_list(parent)

def get_command_doc(key):
    '''
    Returns defined document for the specified command. 
    
    @param key: command key
    
    @rtype: str
    @return: command document
    '''
    
    return get_component(APP_CHANNEL_AUTHORIZER).get_command_doc(key)
