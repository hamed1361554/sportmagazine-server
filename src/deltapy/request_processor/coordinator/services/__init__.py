'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.request_processor.coordinator import APP_TRANSACTION_COORDINATOR

    
def get_request_state(request_id):
    '''
    Returns state of specified request.

    @param str request_id: request ID

    @rtype: int
    @note:
        0: Received
        1: Completed
        2: Failed
        3: Reversed
    @return: request state
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).get_request_state(request_id)

def get_request(request_id):
    '''
    Returns the specified request.

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

    return get_component(APP_TRANSACTION_COORDINATOR).get_request(request_id)

def try_get_request(request_id):
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

    return get_component(APP_TRANSACTION_COORDINATOR).try_get_request(request_id)
    
def get_transaction_detail(transaction_id):
    '''
    Returns detail information of the specified transaction.

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
    @return: transaction detail
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).get_transaction_detail(transaction_id)


def record_request(recorder_type, client_request, **options):
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

    return get_component(APP_TRANSACTION_COORDINATOR).record_request(recorder_type,
                                                                     client_request,
                                                                     **options)


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
    @param dict client_response: client response
    '''
    
    return get_component(APP_TRANSACTION_COORDINATOR).set_completed(recorder_type,
                                                                    client_request,
                                                                    client_response,
                                                                    **options)


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
    @param dict error: error
    '''

    return get_component(APP_TRANSACTION_COORDINATOR).set_failed(recorder_type,
                                                                 client_request,
                                                                 error,
                                                                 **options)


