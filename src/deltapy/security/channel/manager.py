'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

import os

from deltapy.application.services import get_application_dir
from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.event_system.decorators import delta_event
from deltapy.security.session.services import get_current_session
from deltapy.config.manager import ConfigFileNotFoundException
import deltapy.logging.services as logging_services
import deltapy.config.services as config_services
import deltapy.unique_id.services as unique_id_services

class ChannelManagerException(DeltaException):
    pass

class ChannelIsNotRegisteredException(ChannelManagerException):
    pass

class CertificateFileNotFoundException(ChannelManagerException):
    pass


class ChannelManager(DeltaObject):
    '''
    Provides basic functionality to manipulate channels.
    '''
    
    LOGGER = logging_services.get_logger(name='channel')
    
    def __init__(self):
        '''
        '''
        
        DeltaObject.__init__(self)
        
        self._channels = {}
        self._enabled = None
        
    def _get_certificate(self, channel_id, **options):
        '''
        Returns certificate content.
        
        @param channel_id: cannel id.
        @param **options:
            certificate_required: determines whether certificate verification is required. (Default is True)
         
        @rtype: string
        @return: certificate content.

        '''
        
        file_name = '{0}.cert'.format(channel_id).lower() 
        settings_path = os.path.join(get_application_dir(), 'settings')
        certificate_path = os.path.join(settings_path, 'certificates')
        certificate_file = os.path.join(certificate_path, file_name)
        
        certificate_required = options.get('certificate_required')
        if certificate_required is None:
            certificate_required = True
        
        message = 'Loading certificate file [{0}]'
        ChannelManager.LOGGER.debug(message.format(certificate_file))
        if not os.path.exists(certificate_file):
            message = 'Checking certificate required flag is [{0}] for channel [{1}]'
            ChannelManager.LOGGER.debug(message.format(certificate_required, channel_id))
            if certificate_required:
                message = 'Certificate file [{0}] not found.'
                raise CertificateFileNotFoundException(message.format(certificate_file))
            return unique_id_services.get_id('uuid')
        
        certificate = open(certificate_file, 'rb').read()
        return certificate     
        
    def enable_channel(self, channel_id, flag):
        '''
        Enables or disables a channel. 
        
        @param channel_id: channel ID
        @param flag: True or False
        '''
        
        message = 'Trying to enable channel [{0}]'
        if not flag:
            message = 'Trying to disable channel [{0}]'
        ChannelManager.LOGGER.debug(message.format(channel_id))
        
        # Getting channel information
        channel = self.get(channel_id)
        
        # Setting flag
        channel.enabled = flag
        
        message = 'Channel [{0}] enabled successfully'
        if not flag:
            message = 'Channel [{0}] disabled successfully'
        ChannelManager.LOGGER.info(message.format(channel_id))

    def is_registered(self, channel_id):
        '''
        Returns True if the given channel is already registered.
        
        @param channel_id: channel ID
        
        @rtype: bool
        @return: True or False
        '''
        
        return channel_id in self._channels
    
    def get(self, channel_id):
        '''
        Returns channel information according to the given channel ID.
        
        @param channel_id: channel ID
        
        @rtype: DynamicObject<id,
                              description,
                              certificate,
                              certificate_required,
                              enabled>
        @return: channel information
        '''
        
        channel = self._channels.get(channel_id)
        
        if channel is None:
            message = _('Channel [{0}] is not registered.')
            raise ChannelIsNotRegisteredException(message.format(channel_id))
        
        return channel
        
    def try_get_by_certificate(self, certificate):
        '''
        Returns channel information corresponded to the given certificate.
        
        @param certificate: certificate
        
        @rtype: DynamicObject<id,
                              description,
                              certificate,
                              certificate_required,
                              enabled>
        @return: channel information
        '''
        
        for channel in self._channels.values():
            if certificate is not None and \
                channel.certificate.strip() == certificate.strip():
                return channel
            
        return None

    def get_all(self, **options):
        '''
        Returns information of all channels.
        
        @rtype: [DynamicObject<id,
                               description,
                               certificate,
                               certificate_required,
                               enabled>]
        @return: all channels
        '''
        
        return self._channels.values()

    @delta_event('register_channel')
    def register(self, channel_id, certificate, **options):
        '''
        Registers a new channel.
        
        @param channel_id: channel ID
        @param certificate: certificate content
        @param **options: 
            description: channel description
            enabled: channel enable flag
        '''
        
        message = 'Trying to register channel [{0}]'
        ChannelManager.LOGGER.debug(message.format(channel_id))

        # Checking channel existence
        if self.is_registered(channel_id):
            message = _('Channel {0} is already registered.')
            raise ChannelManagerException(message.format(channel_id))
        
        # Checking the previous channel with the same certificate
        registered_channel = \
            self.try_get_by_certificate(certificate)
        if registered_channel is not None:
            message = _('Certificate is in use.')
            raise ChannelManagerException(message)
        
        # Deciding on important parameters
        options['description'] = options.get('description')
        options['enabled'] = options.get('enabled')
        if options['enabled'] is None:
            options['enabled'] = True
        options['certificate_required'] = options.get('certificate_required')
        if options['certificate_required'] is None:
            options['certificate_required'] = True

        # Setting allowed and denied commands            
        options['allowed'] = options.get('allowed')
        options['denied'] = options.get('denied')
        
        # Creating channel information
        channel = DynamicObject(id = channel_id,
                                certificate = certificate)
        channel.update(options)
        
        # Registering channel
        self._channels[channel_id] = channel
        
        message = 'Channel [{0}] successfully registered'
        ChannelManager.LOGGER.info(message.format(channel_id))

    def unregister(self, channel_id, **options):
        '''
        Unregisters a channel.
        
        @param channel_id: channel ID
        '''
        
        message = 'Trying to unregister channel [{0}]'
        ChannelManager.LOGGER.debug(message.format(channel_id))

        # Getting channel information
        channel = self.get(channel_id)
        
        # Unregistering the channel
        self._channels.pop(channel.id)
        
        message = 'Channel [{0}] successfully unregistered'
        ChannelManager.LOGGER.info(message.format(channel_id))
        
    def get_current_channel_id(self):
        '''
        Returns current channel that user logged in with.
        
        @rtype: str
        @return: channel ID
        '''
        
        session = get_current_session()
        context = session.get_context()
        return context.get('channel')
    
    def load(self):
        '''
        Loads all channels.
        '''
        
        try:
            message = 'Loading channels'
            ChannelManager.LOGGER.debug(message)

            config_store = config_services.get_app_config_store('channel')
            self._enabled = config_store.get('global', 'enabled')
            if self._enabled is not None:
                self._enabled = eval(self._enabled)
            else:
                self._enabled = True
                
            if self._enabled:
                for section in config_store.get_sections():
                    if section != 'global':
                        section_data = config_store.get_section_data(section)
                        channel_id = section                        
                        for key in section_data:
                            section_data[key] = eval(str(section_data[key]))
                        
                        certificate = self._get_certificate(channel_id, **section_data)
                        self.register(channel_id, certificate, **section_data)
            else:
                message = 'Channel manager is disabled'
                ChannelManager.LOGGER.info(message)

                
        except ConfigFileNotFoundException:
            message = 'Channel settings not found and channel manager is disabled'
            ChannelManager.LOGGER.info(message)
            self._enabled = False
            
    def is_enable(self):
        '''
        Returns True if the channel manager is enable.
        
        @rtype: bool
        @return: True or False
        '''
        
        return self._enabled
    
