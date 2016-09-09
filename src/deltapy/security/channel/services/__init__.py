'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.security.channel import APP_SECURITY_CHANNEL

def enable_channel(channel_id, flag):
    '''
    Enables or disables a channel. 
    
    @param channel_id: channel ID
    @param flag: True or False
    '''
    
    return get_component(APP_SECURITY_CHANNEL).enable_channel(channel_id, flag)
    
def is_registered(channel_id):
    '''
    Returns True if the given channel is already registered.
    
    @param channel_id: channel ID
    
    @rtype: bool
    @return: True or False
    '''
    
    return get_component(APP_SECURITY_CHANNEL).is_registered(channel_id)

def get(channel_id):
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
    
    return get_component(APP_SECURITY_CHANNEL).get(channel_id)

def try_get_by_certificate(certificate):
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
    
    return get_component(APP_SECURITY_CHANNEL).try_get_by_certificate(certificate)

def get_all(**options):
    '''
    Returns information of all channels.
    
    @rtype: [DynamicObject<id,
                           description,
                           certificate,
                           certificate_required,
                           enabled>]
    @return: all channels
    '''
    
    return get_component(APP_SECURITY_CHANNEL).get_all(**options)

def register(channel_id, certificate, **options):
    '''
    Registers a new channel.
    
    @param channel_id: channel ID
    @param certificate: certificate content
    @param **options: 
        description: channel description
        enabled: channel enable flag
    '''
    
    return get_component(APP_SECURITY_CHANNEL).register(channel_id, certificate, **options)

def unregister(channel_id, **options):
    '''
    Unregisters a channel.
    
    @param channel_id: channel ID
    '''

    return get_component(APP_SECURITY_CHANNEL).unregister(channel_id, **options)

def get_current_channel_id():
    '''
    Returns current channel that user logged in with.
    
    @rtype: str
    @return: channel ID
    '''
    
    return get_component(APP_SECURITY_CHANNEL).get_current_channel_id()
        
def load():
    '''
    Loads all channels.
    '''
    
    return get_component(APP_SECURITY_CHANNEL).load()
        
def is_enable():
    '''
    Returns True if the channel manager is enable.
    
    @rtype: bool
    @return: True or False
    '''

    return get_component(APP_SECURITY_CHANNEL).is_enable()