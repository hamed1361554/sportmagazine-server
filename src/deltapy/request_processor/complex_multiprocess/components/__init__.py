'''
Created on Jan 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.application.decorators import register
from deltapy.request_processor.services import register_processor
from deltapy.request_processor.complex_multiprocess import COMPLEX_MULTI_PROCESS_REQUEST_PROCESSOR
from deltapy.request_processor.complex_multiprocess.processor import ComplexMultiProcessRequestProcessor

@register(COMPLEX_MULTI_PROCESS_REQUEST_PROCESSOR)
class ComplexMultiProcessRequestProcessorComponent(ComplexMultiProcessRequestProcessor):
    '''
    Threaded single process request processor component.
    '''
    
    def __init__(self):
        ComplexMultiProcessRequestProcessor.__init__(self)
        register_processor(self)