'''
Created on Apr 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.request_processor.services import register_processor
from deltapy.request_processor.multithread.processor import MultiThreadedRequestProcessor
from deltapy.request_processor.multithread import MULTI_THREAD_PROCESS_REQUEST_PROCESSOR

@register(MULTI_THREAD_PROCESS_REQUEST_PROCESSOR)
class MultiThreadRequestProcessorComponent(MultiThreadedRequestProcessor):
    '''
    Threaded single process request processor component.
    '''
    
    def __init__(self):
        MultiThreadedRequestProcessor.__init__(self)
        register_processor(self)