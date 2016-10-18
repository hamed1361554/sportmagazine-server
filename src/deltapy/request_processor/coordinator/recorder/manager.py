'''
Created on Apr 23, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.security.channel.services import get_current_channel_id
from deltapy.request_processor.coordinator.recorder.holder import RequestHolder
from deltapy.request_processor.coordinator.recorder.full_recorder import FullRecorder
from deltapy.request_processor.coordinator.recorder.simple_recorder import SimpleRecorder
from deltapy.request_processor.coordinator.coordinator import InvalidRequestIDException


class RequestRecordManagerException(DeltaException):
    '''
    Is raised when request record manager encounters error.
    '''


class RequestRecordManager(DeltaObject):
    '''
    Request Record Manager
    '''

    CURRENT_REQUEST_HEADER_VERSION = 1
    
    def __init__(self):
        '''
        Initializes request record manager.
        '''

        DeltaObject.__init__(self)

        self._recorders = {}
        self._request_holder = None

        self._register_holder()
        self._register_recorders()

    def _register_holder(self):
        '''
        Registers request holder.

        @param object holder: request holder
        '''

        self.register_recorder(RequestHolder())

    def _register_recorders(self):
        '''
        Registers default recorders.
        '''

        self.register_recorder(SimpleRecorder())
        self.register_recorder(FullRecorder())

    def _get_recorder(self, recorder_type):
        '''
        Returns recorder for given recorder type.

        @param str recorder_type: recorder type
        '''

        recorder = self._recorders.get(recorder_type)

        if recorder is None:
            raise RequestRecordManagerException('Recorder [{0}] not found.'.format(recorder_type))

        return recorder

    def _get_request(self, request_id):
        '''
        Fetch request by given ID.

        @param str request_id: request ID
        '''

        request = self._request_holder.try_get(request_id)
        if request is None:
            return None, None
        return request.data.get('request_header'), request

    def _hold_request(self, request, **options):
        '''
        Holds a new request.

        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str client_ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''

        return self._request_holder.hold(request)

    def _get_transaction(self, transaction_id):
        '''
        Fetch transaction by given ID.

        @param str transaction_id: transaction ID
        '''

        return self._request_holder.try_get_transaction(transaction_id)

    def _get_transaction_requests(self, transaction_id):
        '''
        Fetch transaction requests for given ID.

        @param str transaction_id: transaction ID
        '''

        return [(request.data.request_header, request) for request
                in self._request_holder.transaction_requests(transaction_id)]

    def _hold_transaction(self, request, **options):
        '''
        Records a transaction data using the given information.

        @param dict request: request data
        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str client_ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''

        # Getting the existed transaction
        transaction = self._get_transaction(request.transaction_id)

        if transaction is None:
            # Creating transaction if there is no associated transaction
            channel_id = get_current_channel_id()
            transaction = \
                self._create_transaction_data(request.transaction_id,
                                              request.request_date,
                                              channel_id,
                                              request.user_name)
            transaction = self._request_holder.hold_transaction(transaction)
        else:
            # Verifying the current request information with the related transaction
            self._verify_transaction(transaction, request)

        return transaction

    def _verify_transaction(self, transaction, client_request, **options):
        '''
        Verifies transaction using the new request.

        @param dict transaction: transaction data
        @type transaction: dict(str id,
                                datetime creation_date,
                                str channel_id,
                                str user_name)
        @param dict request: request data
        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str client_ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''

        return True

    def _create_transaction_data(self, transaction_id, request_date, channel_id, user_name, **options):
        '''
        Create transaction data.

        @param transaction_id: transaction ID
        @param request_date: request date
        @param channel_id: channel ID
        @param user_name: user name
        '''

        if self._request_holder.contains_transaction(transaction_id):
            raise RequestRecordManagerException('Transaction [{0}] already exists.')

        transaction_data = \
            DynamicObject(transaction_id=transaction_id,
                          request_date=request_date,
                          channel_id=channel_id,
                          user_name=user_name)

        return transaction_data

    def _create_request(self, recorder_type, client_request, **options):
        '''
        Creates request data.

        @param str recorder_type: recorder type
        @param dict client_request: client request
        @param dict client_response: client response
        @param dict error: error

        @return: request data
        '''

        request_header = \
            DynamicObject(recorder_type=recorder_type,
                          version=RequestRecordManager.CURRENT_REQUEST_HEADER_VERSION)

        data = \
            DynamicObject(request_header=request_header)

        request = \
            DynamicObject(request_id=client_request.id,
                          transaction_id=client_request.transaction_id,
                          user_name=client_request.user_name,
                          client_ip=client_request.ip,
                          service_id=client_request.command_key,
                          receieve_date=client_request.recieve_date,
                          request_date=client_request.request_date,
                          trace_id=client_request.trace_id,
                          data=data)

        return request

    def record(self, recorder_type, client_request, **options):
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

        request = \
            self._create_request(recorder_type,
                                 client_request)

        request = \
            self._get_recorder(recorder_type).record(request,
                                                     client_request,
                                                     **options)

        if request is not None:
            self._hold_transaction(request, **options)
            return self._hold_request(request, **options)

    def try_get_by_request_id(self, request_id, **options):
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

        request_header, request = self._get_request(request_id)
        if request_header is None or request is None:
            return None

        return self._get_recorder(request_header.recorder_type).get(request, **options)

    def get_by_request_id(self, request_id, **options):
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

        request = self.try_get_by_request_id(request_id, **options)

        if request is None:
            message = _('Request ID [{0}] is invalid.')
            raise InvalidRequestIDException(message.format(request_id))

        return request
        
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
        @param dict client_response: response data
        '''

        request_header, request = self._get_request(client_request.id)
        if request is None:
            request = \
                self._create_request(recorder_type,
                                     client_request)

        request = \
            self._get_recorder(recorder_type).set_completed(request,
                                                            client_request=client_request,
                                                            client_response=client_response,
                                                            **options)

        self._hold_transaction(request, **options)
        self._request_holder.set_completed(request)

        return request
        
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
        @param str error: error description
        '''

        request_header, request = self._get_request(client_request.id)
        if request is None:
            request = \
                self._create_request(recorder_type,
                                     client_request)

        request = \
            self._get_recorder(recorder_type).set_failed(request,
                                                         client_request=client_request,
                                                         error=error,
                                                         **options)
        self._hold_transaction(request, **options)
        self._request_holder.set_failed(request)

        return request

    def get_by_transaction_id(self, transaction_id, **options):
        '''
        Returns information of a particular transaction.

        @param str transaction_id: transaction ID

        @rtype: dict(str id: transaction ID,
                         datetime creation_date: creation date,
                         str channel_id: channel ID,
                         str user_name: user name)
        @return: transaction data
        '''

        transaction = self._get_transaction(transaction_id)

        if transaction is None:
            message = _('Transaction ID [{0}] is invalid.')
            raise InvalidRequestIDException(message.format(transaction_id))

        return transaction

    def get_detail_by_transaction_id(self, transaction_id, **options):
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

        transaction = self._get_transaction(transaction_id)

        if transaction is None:
            message = _('Transaction ID [{0}] is invalid.')
            raise InvalidRequestIDException(message.format(transaction_id))

        transaction_requests = self._get_transaction_requests(transaction_id)
        transaction.requests = []
        for request_header, request in transaction_requests:
            request = \
                self._get_recorder(request_header.recorder_type).get(request, **options)
            transaction.requests.append(request)

        return transaction

    def get_request_state(self, request_id):
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

        request_header, request = self._get_request(request_id)
        return self._get_recorder(request_header.recorder_type).get_request_state(request)

    def update_request_state(self, request_id, state, **options):
        '''
        Updates the specified request.

        @param str request_id: request ID
        @param int state: request state
        '''

        request_header, request = self._get_request(request_id)

        if request_header is None:
            message = _('Request ID [{0}] is invalid.')
            raise InvalidRequestIDException(message.format(request_id))

        self._request_holder.update_request_state(request, state, **options)

    def register_recorder(self, recorder):
        '''
        Registers request recorder.

        @param object recorder: request recorder
        '''

        self._recorders[recorder.get_name()] = recorder

    def register_holder(self, holder):
        '''
        Registers request holder.

        @param object holder: request holder
        '''

        self._request_holder = holder