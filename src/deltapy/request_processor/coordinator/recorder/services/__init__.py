'''
Created on Apr 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.coordinator.recorder import APP_REQUEST_RECORDER
from deltapy.application.services import get_component

def record(request, **options):
    '''
    Records a request data using the given information.
    
    @param dict request: request data
    @type request: dict(str id: request ID,
                        str transaction_id: transaction ID,
                        str user_name: user name,
                        str ip: client IP,
                        datetime recieve_date: receive date,
                        datetime request_date: request date from client)
    '''

    return get_component(APP_REQUEST_RECORDER).record(request, **options)
    
def get(request_id, **options):
    '''
    Returns information of a particular data.
    
    @param request_id: request ID
    
    @rtype: dict(str id,
                 str transaction_id,
                 datetime request_date,
                 int state,
                 str error)
    @return: request info
    '''
    
    return get_component(APP_REQUEST_RECORDER).get(request_id, **options)
    
def try_get(request_id, **options):
    '''
    Returns information of a particular request and if the request was not found,
    it would return None.
    
    @param request_id: request ID
    
    @rtype: dict(str id,
                 str transaction_id,
                 datetime request_date,
                 int state,
                 str error)
    @return: request info
    '''
    
    return get_component(APP_REQUEST_RECORDER).try_get(request_id, **options)

def set_completed(request_id, **options):
    '''
    Completes the state of the given request.
    
    @param str request_id: request ID
    @param request_id: request ID
    '''
    
    return get_component(APP_REQUEST_RECORDER).set_completed(request_id, **options)
    
def set_failed(request_id, error, **options):
    '''
    Sets the state of the given request to failed.
    
    @param str request_id: request ID
    @param str error: error description 
    '''
    
    return get_component(APP_REQUEST_RECORDER).set_failed(request_id, error, **options)
    
def get_transaction(transaction_id, **options):
    '''
    Returns transaction information.
    
    @param str transaction_id: transaction ID
    
    @rtype: dict(str id,
                 datetime creation_date,
                 str channel_id,
                 str user_name)
    @return: transaction data
    '''
    
    return get_component(APP_REQUEST_RECORDER).get_transaction(transaction_id, **options)

def get_transaction_detail(transaction_id, **options):
    '''
    Returns transaction information.
    
    @param str transaction_id: transaction ID
    
    @rtype: dict(str id,
                 datetime creation_date,
                 str channel_id,
                 str user_name,
                 list requests)
    @type requests: list(dict(str id,
                              datetime request_date,
                              int state,
                              str error) 
    @return: transaction data
    '''

    return get_component(APP_REQUEST_RECORDER).get_transaction_detail(transaction_id, **options)

def get_request_state(request_id):
    '''
    Returns state of specified request.
    
    @param str request_id: request ID
    
    @rtype: int
    @note: 
        0: received
        1: completed
        2: failed
    @return: request state
    '''
    
    return get_component(APP_REQUEST_RECORDER).get_request_state(request_id)