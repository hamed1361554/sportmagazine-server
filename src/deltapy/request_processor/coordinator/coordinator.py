'''
Created on Feb 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.services import add_hook
from deltapy.core import DeltaObject, DeltaEnum, DeltaEnumValue, DeltaException
from deltapy.request_processor.coordinator.commander_hook import \
    TransactionCoordinatorCommandExecutionHook

import deltapy.logging.services as logging_services
import deltapy.request_processor.coordinator.recorder.services as request_recorder_services


class InvalidRequestIDException(DeltaException):
    '''
    Is raised when given request id is not valid.
    '''


class TransactionCoordinator(DeltaObject):
    
    LOGGER = logging_services.get_logger(name='request.coordinator')
    
    class StateEnum(DeltaEnum):
        RECEIVED = DeltaEnumValue(0, 'Received')
        COMPLETED = DeltaEnumValue(1, 'Completed')
        FAILED = DeltaEnumValue(2, 'Failed')
        REVERSED = DeltaEnumValue(3, 'Reversed')
        REVERSE_FAILED = DeltaEnumValue(4, 'Reversed Failed')
        
    def __init__(self):
        '''
        Initializes transaction coordinator.
        '''

        DeltaObject.__init__(self)

        add_hook(TransactionCoordinatorCommandExecutionHook())

    def get_request(self, request_id):
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

        return request_recorder_services.get_by_request_id(request_id)

    def try_get_request(self, request_id, **options):
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

        return request_recorder_services.try_get_by_request_id(request_id, **options)
                        
    def get_request_state(self, request_id):
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
        
        return request_recorder_services.get_request_state(request_id)

    def get_transaction_detail(self, transaction_id):
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

        return request_recorder_services.get_detail_by_transaction_id(transaction_id)

    def record_request(self, recorder_type, client_request, **options):
        '''
        Records a request data using the given information.

        @param str recorder_type: recorder type
        @type client_request: dict(str id: request ID,
                               str transaction_id: transaction ID,
                               str user_name: user name,
                               str client_ip: client IP,
                               datetime receive_date: receive date,
                               datetime request_date: request date from client)
        @param dict client_request: request data
        '''

        request_recorder_services.record(recorder_type,
                                         client_request,
                                         **options)
        
    def set_completed(self, recorder_type, client_request, client_response, **options):
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

        request_recorder_services.set_completed(recorder_type,
                                                client_request,
                                                client_response,
                                                **options)
        
    def set_failed(self, recorder_type, client_request, error, **options):
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
        @param duct error: error
        '''

        request_recorder_services.set_failed(recorder_type,
                                             client_request,
                                             error,
                                             **options)
