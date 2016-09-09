'''
Created on May 1, 2013

@author: ehsan
'''

from deltapy.event_system.decorators import after_handler
import deltapy.request_processor.coordinator.services as coordinator_services

@after_handler('register_channel', 'request_processor.coordinator.add')
def register_channel_handler(event_args):
    '''
    Starts communicator.
    '''

    channel_id = event_args['args'][1]
    
    return coordinator_services.add_channel(channel_id)

