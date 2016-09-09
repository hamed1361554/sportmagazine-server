'''
Created on Feb, 2015

@author: Aidin
'''

from deltapy.application.decorators import register
from deltapy.request_processor.single_process import SINGLE_PROCESS
from deltapy.request_processor.single_process.processor import SingleProcessRequestProcessor
from deltapy.request_processor.services import register_processor


@register(SINGLE_PROCESS)
class SingleProcessRequestProcessorComponent(SingleProcessRequestProcessor):
    '''
    '''

    def __init__(self):
        SingleProcessRequestProcessor.__init__(self)
        register_processor(self)
