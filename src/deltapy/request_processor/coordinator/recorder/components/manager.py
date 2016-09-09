'''
Created on Apr 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.coordinator.recorder.manager import RequestRecordManager
from deltapy.application.decorators import register
from deltapy.request_processor.coordinator.recorder import APP_REQUEST_RECORDER

@register(APP_REQUEST_RECORDER)
class RequestRecordManagerComponent(RequestRecordManager):
    pass