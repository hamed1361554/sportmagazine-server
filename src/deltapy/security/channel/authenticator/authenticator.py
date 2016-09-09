'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException
import deltapy.security.session.services as session_services
import deltapy.security.channel.services as channel_services
import deltapy.logging.services as logging_services

class ChannelAuthenicationException(DeltaException):
    pass

class ChannelAuthenicator(DeltaObject):
    '''
    Handles channel authentication.
    '''
    
    LOGGER = logging_services.get_logger(name='channel')
    
    def _verify_channel(self, channel, **options):
        '''
        Verifies general conditions on the given channel
        
        @param channel: channel instance
        '''

        # Verifying channel
        if channel is None:
            raise ChannelAuthenicationException(_('Channel authentication failed. Please revise your certificate.'))
        if not channel.enabled:
            raise ChannelAuthenicationException(_('Channel authentication failed. Channel is disable.'))

    def authenticate(self, ticket, certificate, **options):
        '''
        Authenticates a certificate considering the given ticket.
        
        @param ticket: ticket
        @param certificate: certificate
        '''
        
        # Getting session
        session = session_services.get_session(ticket, False)
        
        # Getting current user
        current_user = session.get_user()

        if channel_services.is_enable():
            # Getting login parameters
            given_channel_id = options.get('channel')
            given_channel = None
            if given_channel_id is not None:
                given_channel = channel_services.get(given_channel_id)
                if not given_channel.certificate_required:
                    # Verifying channel
                    self._verify_channel(given_channel)
                    
                    # Setting channel ID
                    self._set_channel_to_session(ticket, given_channel_id)     
                    
                    message = 'User [{0}] authenticated through risky channel [{1}]'
                    ChannelAuthenicator.LOGGER.warning(message.format(current_user.id, given_channel_id))
                    
                    return
                    
            # Getting channel info using certificate
            channel = channel_services.try_get_by_certificate(certificate)

            # Verifying channel
            self._verify_channel(channel)

            # Logging
            message = 'Authenticating User [{0}] using certification [{1}]'
            ChannelAuthenicator.LOGGER.info(message.format(current_user.id, certificate))

            if given_channel is not None and given_channel.id != channel.id:
                raise ChannelAuthenicationException(_('Channel authentication failed. Channel mismatched.'))
            
            # Setting channel ID
            self._set_channel_to_session(ticket, channel.id)
                      
            message = 'User [{0}] authenticated with certified channel [{1}]'
            ChannelAuthenicator.LOGGER.warning(message.format(current_user.id, channel.id))
            
    def _set_channel_to_session(self, ticket, channel_id, **options):
        '''
        Sets channel to session using the given ticket.
        
        @param ticket: ticket
        @param channel_id: channel ID
        '''
        
        # Getting session
        session = session_services.get_session(ticket, False)
        
        # Getting session context to set user channel
        context = session.get_context()

        # Setting channel ID            
        context['channel'] = channel_id
        
        # Updating session to apply changes
        session.update()
        
