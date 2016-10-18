'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.request_processor.coordinator.services as coordinator_services

@command('request_processor.coordinator.request')
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

    return coordinator_services.get_request(request_id)
    
@command('request_processor.coordinator.request.state')
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
    
    return coordinator_services.get_request_state(request_id)    
    
@command('request_processor.coordinator.transaction.detail')
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
    
    return coordinator_services.get_transaction_detail(transaction_id)    
