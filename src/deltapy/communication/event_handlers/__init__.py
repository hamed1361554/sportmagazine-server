'''
Created on May 30, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.event_system.decorators import after_handler
import deltapy.communication.services as communication_services 

@after_handler('application.start', 'communication.start')
def application_start_handler(params):
    '''
    Starts communicator.
    '''
    
    return communication_services.start()


@after_handler('application.stop', 'communication.stop')
def application_stop_handler(params):
    '''
    Stops communicator.
    '''

    communication_services.stop(force=True)
