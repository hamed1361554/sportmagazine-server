'''
Created on Jan 17, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class RequestProcessorManagerHook(DeltaObject):
    '''
    It is a hook to monitor request processor behavior.
    '''
    
    def __init__(self, name):
        DeltaObject.__init__(self)
        self._set_name_(name)
    
    def on_process(self, request, **options):
        '''
        It will be called when a request starts to be processed
        
        @param ClientRequest request: client request
        '''
        
    def on_process_completed(self, request, response, **options):
        '''
        It will be called when a request is completed.
        
        @param ClientRequest request: client request
        @param ServerResponse response: server response
        '''
        
    def on_process_failed(self, request, error, **options):
        '''
        It will be called when a request is failed.
        
        @param ClientRequest request: client request
        @param Exception error: error content
        '''
        