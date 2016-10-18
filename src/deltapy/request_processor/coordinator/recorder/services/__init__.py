'''
Created on Apr 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.request_processor.coordinator.recorder import APP_REQUEST_RECORDER


def register_holder(holder):
    '''
    Registers request holder.

    @param object holder: request holder
    '''

    return get_component(APP_REQUEST_RECORDER).register_holder(holder)

def register_recorder(recorder):
    '''
    Registers request recorder.

    @param object recorder: request recorder
    '''

    return get_component(APP_REQUEST_RECORDER).register_recorder(recorder)

def record(recorder_type, client_request, **options):
    '''
    Records a request data using the given information.

    @param str recorder_type: recorder type
    @param dict client_request: request data
    @type client_request: dict(str id: request ID,
                               str transaction_id: transaction ID,
                               str user_name: user name,
                               str client_ip: client IP,
                               datetime receive_date: receive date,
                               datetime request_date: request date from client)
    '''

    return get_component(APP_REQUEST_RECORDER).record(recorder_type, client_request, **options)
    
def get(recorder_type, request_id, **options):
    '''
    Returns information of a particular request.

    @param str recorder_type: recorder type
    @param request_id: request ID

    @rtype: dict(str request_id: client request ID,
                 str transaction_id: client request transaction ID,
                 str user_name: client request user name,
                 str client_ip: client request IP,
                 str service_id: client request service ID,
                 datetime receieve_date: client request recieve date,
                 datetime request_date: client request request date,
                 str trace_id: client request trace ID,
                 int state: request state,
                 dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: request info
    '''
    
    return get_component(APP_REQUEST_RECORDER).get(recorder_type, request_id, **options)

def get_by_request_id(request_id, **options):
    '''
    Returns information of a particular request.

    @param str request_id: request ID

    @rtype: dict(str request_id: client request ID,
                 str transaction_id: client request transaction ID,
                 str user_name: client request user name,
                 str client_ip: client request IP,
                 str service_id: client request service ID,
                 datetime receieve_date: client request recieve date,
                 datetime request_date: client request request date,
                 str trace_id: client request trace ID,
                 int state: request state,
                 dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: request info
    '''

    return get_component(APP_REQUEST_RECORDER).get_by_request_id(request_id, **options)
    
def try_get(recorder_type, request_id, **options):
    '''
    Returns information of a particular request and if the request was not found,
    it would return None.

    @param str recorder_type: recorder type
    @param str request_id: request ID
    
    @rtype: dict(str request_id: client request ID,
                 str transaction_id: client request transaction ID,
                 str user_name: client request user name,
                 str client_ip: client request IP,
                 str service_id: client request service ID,
                 datetime receieve_date: client request recieve date,
                 datetime request_date: client request request date,
                 str trace_id: client request trace ID,
                 int state: request state,
                 dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: request info
    '''
    
    return get_component(APP_REQUEST_RECORDER).try_get(recorder_type, request_id, **options)

def try_get_by_request_id(request_id, **options):
    '''
    Returns information of a particular request.

    @param str request_id: request ID

    @rtype: dict(str request_id: client request ID,
                 str transaction_id: client request transaction ID,
                 str user_name: client request user name,
                 str client_ip: client request IP,
                 str service_id: client request service ID,
                 datetime receieve_date: client request recieve date,
                 datetime request_date: client request request date,
                 str trace_id: client request trace ID,
                 int state: request state,
                 dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: request info
    '''

    return get_component(APP_REQUEST_RECORDER).try_get_by_request_id(request_id, **options)

def set_completed(recorder_type, client_request, client_response, **options):
    '''
    Completes the state of the given request.

    @param str recorder_type: recorder type
    @param dict client_request: request data
    @type client_request: dict(str id: request ID,
                               str transaction_id: transaction ID,
                               str user_name: user name,
                               str client_ip: client IP,
                               datetime receive_date: receive date,
                               datetime request_date: request date from client)
    @param dict client_response: response data
    '''
    
    return get_component(APP_REQUEST_RECORDER).set_completed(recorder_type, client_request, client_response, **options)
    
def set_failed(recorder_type, client_request, error, **options):
    '''
    Sets the state of the given request to failed.

    @param str recorder_type: recorder type
    @param dict client_request: request data
    @type client_request: dict(str id: request ID,
                               str transaction_id: transaction ID,
                               str user_name: user name,
                               str client_ip: client IP,
                               datetime receive_date: receive date,
                               datetime request_date: request date from client)
    @param str error: error description
    '''
    
    return get_component(APP_REQUEST_RECORDER).set_failed(recorder_type, client_request, error, **options)
    
def get_transaction(recorder_type, transaction_id, **options):
    '''
    Returns transaction information.

    @param str recorder_type: recorder type
    @param str transaction_id: transaction ID
    
    @rtype: dict(str id: transaction ID,
                 datetime creation_date: creation date,
                 str channel_id: channel ID,
                 str user_name: user name)
    @return: transaction data
    '''
    
    return get_component(APP_REQUEST_RECORDER).get_transaction(recorder_type, transaction_id, **options)

def get_by_transaction_id(transaction_id, **options):
    '''
    Returns information of a particular transaction.

    @param str transaction_id: transaction ID

    @rtype: dict(str id: transaction ID,
                     datetime creation_date: creation date,
                     str channel_id: channel ID,
                     str user_name: user name)
    @return: transaction data
    '''

    return get_component(APP_REQUEST_RECORDER).get_by_transaction_id(transaction_id, **options)

def get_transaction_detail(recorder_type, transaction_id, **options):
    '''
    Returns transaction information.

    @param str recorder_type: recorder type
    @param str transaction_id: transaction ID
    
    @rtype: dict(str transaction_id: transaction ID
                 datetime start_date: start date of transaction,
                 str user_id: user ID,
                 list(dict) requests: requests regarding to the transaction)
    @type request: dict(str request_id: client request ID,
                        str transaction_id: client request transaction ID,
                        str user_name: client request user name,
                        str client_ip: client request IP,
                        str service_id: client request service ID,
                        datetime receieve_date: client request recieve date,
                        datetime request_date: client request request date,
                        str trace_id: client request trace ID,
                        int state: request state,
                        dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: transaction data
    '''

    return get_component(APP_REQUEST_RECORDER).get_transaction_detail(recorder_type, transaction_id, **options)

def get_detail_by_transaction_id(transaction_id, **options):
    '''
    Returns detail information of a particular transaction.

    @param str transaction_id: tranasction ID

    @rtype: dict(str transaction_id: transaction ID
                 datetime start_date: start date of transaction,
                 str user_id: user ID,
                 list(dict) requests: requests regarding to the transaction)
    @type request: dict(str request_id: client request ID,
                        str transaction_id: client request transaction ID,
                        str user_name: client request user name,
                        str client_ip: client request IP,
                        str service_id: client request service ID,
                        datetime receieve_date: client request recieve date,
                        datetime request_date: client request request date,
                        str trace_id: client request trace ID,
                        int state: request state,
                        dict data: data)
    @type data: dict(dict request_header: request header,
                     dict command_args: command args,
                     dict command_kwargs: command kwargs,
                     dict call_context: call context,
                     dict response_data: response data
                     str error: error)
    @type request_header: dict(str recorder_type: recorder type,
                               int version: version)
    @type response_data: dict(datetime send_date: client response send date,
                              dict command_result: client response command result)
    @return: transaction data
    '''

    return get_component(APP_REQUEST_RECORDER).get_detail_by_transaction_id(transaction_id, **options)

def get_request_state(request_id):
    '''
    Returns state of specified request.
    
    @param str request_id: request ID
    
    @rtype: int
    @note: 
        0: received
        1: completed
        2: failed
        3: reversed
    @return: request state
    '''
    
    return get_component(APP_REQUEST_RECORDER).get_request_state(request_id)

def update_request_state(request_id, state, **options):
    '''
    Updates the specified request.

    @param str request_id: request ID
    @param int state: request state
    '''

    return get_component(APP_REQUEST_RECORDER).update_request_state(request_id, state, **options)