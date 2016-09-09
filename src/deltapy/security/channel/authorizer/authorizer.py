'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

import fnmatch

from deltapy.core import DeltaObject, DeltaException
from deltapy.caching.decorators import cache
from deltapy.security.channel.authorizer.command_hook import ChannelAuthorizerCommandHook
from deltapy.security.channel.services import get_current_channel_id
import deltapy.security.channel.services as channel_services
import deltapy.commander.services as commander_services
import deltapy.logging.services as logging_services

class ChannelAuthorizerException(DeltaException):
    pass

class ChannelAccessDenied(ChannelAuthorizerException):
    pass

class ChannelAuthorizer(DeltaObject):
    '''
    It is responsible to provide functionality to limit services on user channels.
    '''
    
    LOGGER = logging_services.get_logger(name='channel')
    GLOBAL_ALLOWED = ['app.introduce',
                      'command.list',
                      'command.doc',
                      'security.authenticate',
                      'request_processor.coordinator.request.state']
    
    def __init__(self):
        DeltaObject.__init__(self)
        
        commander_services.add_hook(ChannelAuthorizerCommandHook())

    def _get_commands(self, pattern, all_commands):
        '''
        Returns list of commands according to the given pattern.
        
        @param pattern: pattern
        
        @rtype: [str]
        @return: commands
        '''
        
        result = []
        for command in all_commands:
            if fnmatch.fnmatch(command, pattern.strip()):
                result.append(command)
        return result
    
    def _get_allowed_commands(self, channel_id):
        '''
        Returns allowed commands on the given channel.
        
        @param channel_id: channel ID
        
        @rtype: [str]
        @return: allowed commands 
        '''
        
        channel = channel_services.get(channel_id)
        
        if channel.allowed is None or len(channel.allowed.strip()) == 0:
            channel.allowed = '*'
            
        allowed_commands = channel.allowed.replace(';', ',').split(',')
        
        result = []
        for pattern in allowed_commands:
            result.extend(self._get_commands(pattern, self._get_all_commands()))
        return set(result)
        
    def _get_denied_commands(self, channel_id):
        '''
        Returns denied commands on the given channel.
        
        @param channel_id: channel ID
        
        @rtype: list<str>
        @return: denied commands 
        '''
        
        channel = channel_services.get(channel_id)
        
        if channel.denied is None or len(channel.denied.strip()) == 0:
            return set([])

        denied_commands = channel.denied.replace(';', ',').split(',')
        result = []
        for pattern in denied_commands:
            result.extend(self._get_commands(pattern, self._get_all_commands()))
        return set(result)

    def _get_all_commands(self):
        '''
        Returns all of application commands
        
        @rtype: [str]
        @return: command list
        '''

        result = []
        
        for command in commander_services.get_commands():
            result.append(command.get_key())
            
        return result
    
    @cache
    def get_channel_authorized_commands(self, channel_id):
        '''
        Returns all authorized command on the given channel.
        
        @param channel_id: channel ID
        '''
        
        allowed = set(self._get_allowed_commands(channel_id))
        #ChannelAuthorizer.LOGGER.debug('allowed:{0}'.format(allowed))
        denied = set(self._get_denied_commands(channel_id))
        #ChannelAuthorizer.LOGGER.debug('denied:{0}'.format(denied))
        return allowed.difference(denied).union(set(ChannelAuthorizer.GLOBAL_ALLOWED))
    
    def authorize(self, channel_id, command_key, **options):
        '''
        Authorizes the given command on the specified channel.
        
        @param channel_id: channel ID
        @param command_key: command key
        '''

        if channel_services.is_enable():
            # Getting command instance        
            command = commander_services.get_command(command_key)
            if command is None:
                message = _('Command [{0}] not found.')
                raise ChannelAuthorizerException(message.format(command_key))
            
            ChannelAuthorizer.LOGGER.debug('Authorizing command [{0}] on channel [{1}]'.format(command_key, channel_id))
            if command.get_key() not in self.get_channel_authorized_commands(channel_id):
                message = _('Channel [{0}] has not access on command [{1}].')
                raise ChannelAccessDenied(message.format(channel_id, command_key))
            ChannelAuthorizer.LOGGER.info('Command [{0}] authorized on channel [{1}]'.format(command_key, channel_id))
    
    def get_command_list(self, parent = None): 
        '''
        Returns available commands list.
        
        @param parent: parent command
        
        @rtype: [str]
        @return: command list
        '''
        
        result = []
        for command in commander_services.get_commands(parent):
            result.append(command.get_key())

        if not channel_services.is_enable():
            return result
        
        allowed = self.get_channel_authorized_commands(get_current_channel_id())
        return list(set(allowed).intersection(set(result)))
    
    def get_command_doc(self, key):
        '''
        Returns defined document for the specified command. 
        
        @param key: command key
        
        @rtype: str
        @return: command document
        '''
        
        # Getting command instance        
        command = commander_services.get_command(key)
        if command is None:
            message = _('Command [{0}] not found.')
            raise ChannelAuthorizerException(message.format(key))

        if channel_services.is_enable():
            # Authorizing the command
            self.authorize(get_current_channel_id(), key)
        
        return command.get_doc()