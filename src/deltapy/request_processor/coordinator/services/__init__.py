'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.coordinator import APP_TRANSACTION_COORDINATOR
from deltapy.application.services import get_component

def get_transaction_state(transaction_id):
    '''
    Returns transaction state.
    
    @param str transaction_id: transaction ID
    
    @rtype: int
    @note: 
        0: Received
        1: Completed
        2: Failed
    @return: transaction state
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).get_transaction_state(transaction_id)
    
def get_request_state(request_id):
    '''
    Returns reuqest state.
    
    @param str request_id: request ID
    
    @rtype: int
    @note: 
        0: Received
        1: Completed
        2: Failed
    @return: transaction state
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).get_request_state(request_id)    
    
def get_transaction_detail(transaction_id):
    '''
    Returns detail information of the specified transaction.
    
    @param str transaction_id: transaction ID
    
    @rtype: dict(str transaction_id: transaction ID
                 int state: transaction state,
                 datetime start_date: start date of transaction,
                 str user_id: user ID,
                 list requests: requests regarding to the transaction)
    @type requests: dict(str request_id: request ID,
                         int state: request state,
                         object input: request input,
                         object result: request result)
                         
    @return: transaction detail
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).get_transaction_detail(transaction_id)    
    
def activate_channel(channel_id):
    '''
    Activates transaction coordination on the given channel. 
    
    @param str channel_id: channel ID
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).activate_channel(channel_id)
    
def activate_service(channel_id, service_id):
    '''
    Activates transaction coordination on the given service.
    
    @param str channel_id: channel ID
    @param str service_id: service ID
    '''
           
    return get_component(APP_TRANSACTION_COORDINATOR).activate_service(service_id)

def deactivate_channel(channel_id):
    '''
    Deativates transaction coordination on the given channel. 
    
    @param str channel_id: channel ID
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).deactivate_channel(channel_id)

def deactivate_service(service_id):
    '''
    Dectivates transaction coordination on the given service.
    
    @param str channel_id: channel ID
    @param str service_id: service ID
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).deactivate_service(service_id)

def update_request_state(request_id, state, **options):
    '''
    Updates the state of the given request.
    
    @param str request_id: request ID
    @param int state: request state
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).update_request_state(request_id, state, **options)

def record_request(request, **options):
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

    return get_component(APP_TRANSACTION_COORDINATOR).record_request(request, **options)

def set_completed(request, **options):
    '''
    Completes the state of the given request.
    
    @param str request_id: request ID
    @param request_id: request ID
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).set_completed(request, **options)

def set_failed(request, error, **options):
    '''
    Sets the state of the given request to failed.
    
    @param str request_id: request ID
    @param str error: error description 
    '''

    return get_component(APP_TRANSACTION_COORDINATOR).set_failed(request, error, **options)

def load():
    '''
    Loads activated channels and services. 
    '''

    return get_component(APP_TRANSACTION_COORDINATOR).load()

def add_channel(channel_id):
    """
    Adds a channel to coordinator.

    @param str channel_id: channel id
    """

    return get_component(APP_TRANSACTION_COORDINATOR).add_channel(channel_id)
