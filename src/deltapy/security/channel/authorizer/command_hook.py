'''
Created on Feb 2, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.channel.services import get_current_channel_id
from deltapy.commander.hook import CommandExecutionHook
from deltapy.security.channel.authorizer.services import authorize 

class ChannelAuthorizerCommandHook(CommandExecutionHook):
    '''
    It is a command hook that authorizes command on the current channel.
    '''
    
    def before_execute(self, commander, command, *args, **kargs):
        '''
        This method will be called before command execution.
        
        @param commander: commander
        @param command: command
        '''

        channel_id = get_current_channel_id()
        authorize(channel_id, command.get_key())
        