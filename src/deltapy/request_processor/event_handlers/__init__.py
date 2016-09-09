'''
Created on May 30, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.event_system.decorators import after_handler
import deltapy.request_processor.services as request_processor

@after_handler('application.start', 'request_processor.start')
def application_start_handler(params):
    '''
    Starts request processor.
    '''
    
    return request_processor.start()


@after_handler('application.stop', 'request_processor.terminate')
def application_stop_handler(params):
    '''
    Terminates request processor.
    '''
    
    return request_processor.terminate()

