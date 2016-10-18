'''
Created on Apr 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.request_processor.coordinator.recorder import APP_REQUEST_RECORDER
from deltapy.request_processor.coordinator.recorder.manager import RequestRecordManager


@register(APP_REQUEST_RECORDER)
class RequestRecordManagerComponent(RequestRecordManager):
    '''
    Request Record Manager Component
    '''
