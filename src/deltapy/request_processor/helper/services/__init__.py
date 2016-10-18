"""
Created on 11/25/15

@author: Ehsan F.J
"""
from deltapy.application.services import get_component
from deltapy.request_processor.helper import REQUEST_PROCESSOR_HELPER


def set_request_timeout(timeout):
    """
    Sets request timeout in current thread.
    """

    return get_component(REQUEST_PROCESSOR_HELPER).set_request_timeout(timeout)
