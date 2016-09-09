'''
Created on Apr 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.hook import RequestProcessorManagerHook

import deltapy.request_processor.coordinator.services as coordinator_services
import deltapy.logging.services as logging_services

class TransactionCoordinatorRequestProcessorManagerHook(RequestProcessorManagerHook):
    
    LOGGER = logging_services.get_logger(name='request.coordinator')
    
    def __init__(self):
        RequestProcessorManagerHook.__init__(self, 'request_processor_manager.hook.coordinator')
    
    def on_process(self, request, **options):
        '''
        It will be called when a request starts to be processed
        
        @param ClientRequest request: client request
        '''
        
        coordinator_services.record_request(request)
        logging_services.debug('Request [{0}] for service [{1}] recorded.'.format(request.id, request.command_key))
        
    def on_process_completed(self, request, response, **options):
        '''
        It will be called when a request is completed.
        
        @param ClientRequest request: client request
        @param ServerResponse response: server response
        '''
        
        coordinator_services.set_completed(request)
        logging_services.debug('Request [{0}] for service [{1}] completed.'.format(request.id, request.command_key))
        
    def on_process_failed(self, request, error, **options):
        '''
        It will be called when a request is failed.
        
        @param ClientRequest request: client request
        @param Exception error: error content
        '''

        coordinator_services.set_failed(request, error.message)
        logging_services.debug('Request [{0}] for service [{1}] failed.'.format(request.id, request.command_key))
        