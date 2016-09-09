'''
Created on Jan 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.application.decorators import register
from deltapy.request_processor import APP_REQUEST_PROCESSOR
from deltapy.request_processor.manager import RequestProcessorManager

@register(APP_REQUEST_PROCESSOR)
class RequestProcessorManagerComponent(RequestProcessorManager):
    '''
    Request processor Manager Component
    '''