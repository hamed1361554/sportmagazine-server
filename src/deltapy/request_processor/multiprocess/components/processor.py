'''
Created on Apr 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.request_processor.services import register_processor
from deltapy.request_processor.multiprocess import MULTI_PROCESS_REQUEST_PROCESSOR
from deltapy.request_processor.multiprocess.processor import MultiProcessRequestProcessor

@register(MULTI_PROCESS_REQUEST_PROCESSOR)
class MultiThreadedProcessRequestProcessorComponent(MultiProcessRequestProcessor):
    '''
    Threaded single process request processor component.
    '''
    
    def __init__(self):
        MultiProcessRequestProcessor.__init__(self)
        register_processor(self)