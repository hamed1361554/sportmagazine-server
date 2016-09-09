'''
Created on Oct 15, 2014

@author: Abi.Mohammadi
'''

from deltapy.request_processor.zmq.processor import ZMQRequestProcessor
from deltapy.application.decorators import register
from deltapy.request_processor.zmq import ZMQ_REQUEST_PROCESSOR
from deltapy.request_processor.services import register_processor

@register(ZMQ_REQUEST_PROCESSOR)
class ZMQRequestProcessorComponent(ZMQRequestProcessor):
    def __init__(self):
        ZMQRequestProcessor.__init__(self)
        register_processor(self)