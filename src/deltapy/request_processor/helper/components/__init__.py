"""
Created on 11/25/15

@author: Ehsan F.J
"""

from deltapy.application.decorators import register
from deltapy.request_processor.helper import REQUEST_PROCESSOR_HELPER
from deltapy.request_processor.helper.helper import RequestProcessorHelper

@register(REQUEST_PROCESSOR_HELPER)
class RequestProcessorHelperComponent(RequestProcessorHelper):
    '''
    Request processor helper Component
    '''