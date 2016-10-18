'''
Created on July 4, 2016

@author: Hamed
'''

from deltapy.core import DeltaObject, DeltaException
from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator


class RequestHolderException(DeltaException):
    '''
    Is raised when request holder encounters and error.
    '''


class RequestHolder(DeltaObject):

    def __init__(self):
        '''
        Initializes request holder.
        '''

        DeltaObject.__init__(self)

        self._transactions = {}
        self._requests = {}

    def _get(self, request_id, default=None):
        '''
        Returns request detail for given ID.

        @param str request_id:
        @param object default: default object

        @rtype: dict
        @return: request detail
        '''

        request = self._requests.get(request_id)

        if request is None:
            return default

        return request

    def _get_transaction(self, transaction_id, default=None):
        '''
        Returns transaction detail for given ID.

        @param str transaction_id: transaction ID
        @param object default: default object

        @rtype: dict
        @return: transaction detail
        '''

        transaction = self._transactions.get(transaction_id)

        if transaction is None:
            return default

        return transaction

    def get(self, request_id, default=None, raise_error=True):
        '''
        Returns request detail for given ID.

        @param str request_id:
        @param object default: default object
        @param bool raise_error: flag to raise error

        @rtype: dict
        @return: request detail
        '''

        request = self._get(request_id, default=default)

        if raise_error and request is None:
            raise RequestHolderException("No request found with given request id [[0]]".format(request_id))

        return request

    def get_transaction(self, transaction_id, default=None, raise_error=True):
        '''
        Returns transaction detail for given ID.

        @param str transaction_id: transaction ID
        @param object default: default object
        @param bool raise_error: flag to raise error

        @rtype: dict
        @return: transaction detail
        '''

        transaction = self._get_transaction(transaction_id, default=default)

        if raise_error and transaction is None:
            raise RequestHolderException("No transaction found with given id [{0}]".format(transaction_id))

        return transaction

    def try_get(self, request_id, default=None):
        '''
        Returns request detail for given ID.

        @param str request_id:
        @param object default: default object

        @rtype: dict
        @return: request detail
        '''

        return self.get(request_id, default=default, raise_error=False)

    def try_get_transaction(self, transaction_id, default=None):
        '''
        Returns transaction detail for given ID.

        @param str transaction_id: transaction ID
        @param object default: default object

        @rtype: dict
        @return: transaction detail
        '''

        return self.get_transaction(transaction_id, default=default, raise_error=False)

    def transaction_requests(self, transaction_id):
        '''
        Returns all stored request details for given transaction ID.

        @rtype: list(dict)
        @return: all stored transaction details
        '''

        return [request for id, request in self._requests.iteritems()
                if request.transaction_id == transaction_id]

    def contains(self, request_id):
        '''
        Determines whether given request exists.

        @param str transaction_id: request ID
        '''

        return request_id in self._requests

    def contains_transaction(self, transaction_id):
        '''
        Determines whether given transaction exists.

        @param str transaction_id: transaction ID
        '''

        return transaction_id in self._transactions

    def hold(self, request):
        '''
        Holds given request.

        @param dict request: request data
        '''

        self._requests[request.request_id] = request
        return request

    def hold_transaction(self, transaction):
        '''
        Holds given transaction.

        @param dict transaction: transaction data
        '''

        self._transactions[transaction.transaction_id] = transaction
        return transaction

    def set_completed(self, request, **options):
        '''
        Completes the state of the given request.

        @param dict request: request
        '''

        self._update_request(request,
                             TransactionCoordinator.StateEnum.COMPLETED,
                             **options)

    def set_failed(self, request, **options):
        '''
        Sets the state of the given request to failed.

        @param dict request: request
        '''

        self._update_request(request,
                             TransactionCoordinator.StateEnum.FAILED,
                             **options)

    def update_request_state(self, request, state, **options):
        '''
        Updates the specified request.

        @param dict request: request
        @param int state: request state
        '''

        return self._update_request(request, state, **options)

    def _update_request(self, request, state, **options):
        '''
        Updates the specified request.

        @param str request_id: request ID
        @param int state: request state
        @keyword str error: error description
        '''

        request.state = state
        return self.hold(request)
