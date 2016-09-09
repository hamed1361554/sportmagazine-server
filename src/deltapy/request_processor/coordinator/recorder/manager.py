'''
Created on Apr 23, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DynamicObject, DeltaException
from deltapy.security.channel.services import get_current_channel_id
from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator

class RequestRecordManagerException(DeltaException):
    pass

class InvalidRequestIDException(RequestRecordManagerException):
    pass

class RequestRecordManager(DeltaObject):
    
    def __init__(self):
        '''
        '''

        self._transactions = {}
        self._requests = {}
        
    def _try_get_transaction(self, transaction_id):
        '''
        Returns transaction information, if transaction exists otherwise returns None
        
        @param str transaction_id: transaction ID
        
        @rtype: dict(str id,
                     datetime creation_date,
                     str channel_id,
                     str user_name)
        @return: transaction data
        '''
        
        return self._transactions.get(transaction_id)
    
    def _verify_transaction(self, transaction, request):
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
                            str ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''
        
    def _create_request(self, request):
        '''
        Records the request.
        
        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''
        
        request_data = \
            DynamicObject(id=request.id,
                          transaction_id=request.transaction_id,
                          user_name=request.user_name,
                          ip=request.ip,
                          recieve_date=request.recieve_date,
                          request_date=request.request_date)
        self._requests[request.id] = request_data
        return request_data
        
    def _create_transaction(self, transaction_id, request_date, channel_id, user_name, **options):
        '''
        Creates a new transaction.
        
        @param transaction_id: transaction ID
        @param request_date: request date
        @param channel_id: channel ID
        @param user_name: user name
        '''
        
        if transaction_id in self._transactions:
            raise RequestRecordManagerException('Transaction [{0}] already exists.')
        
        transaction = \
            DynamicObject(id=transaction_id, 
                          request_date=request_date, 
                          channel_id=channel_id, 
                          user_name=user_name)
        self._transactions[transaction_id] = transaction
        return transaction
        
    def record(self, request, **options):
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

        # Getting the existed transaction        
        transaction = self._try_get_transaction(request.transaction_id)
        channel_id = get_current_channel_id()
        if transaction is None:
            # Creating transaction if there is no associated transaction
            self._create_transaction(request.transaction_id, request.request_date, channel_id, request.user_name)
        else:
            # Verifying the current request information with the related transaction 
            self._verify_transaction(transaction, request)
            
        # Creating request
        self._create_request(request)
        
    def _update_request(self, request_id, state, **options):
        '''
        Updates the specified request.
        
        @param str request_id: request ID
        @param int state: request state
        @keyword str error: error description
        '''
        
        request = self.get(request_id)
        request.state = state
        request.error = options.get('error')
        
    def try_get(self, request_id, **options):
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
        
        return self._requests.get(request_id)

    def get(self, request_id, **options):
        '''
        Returns information of a particular request.
        
        @param request_id: request ID
        
        @rtype: dict(str id,
                     str transaction_id,
                     datetime request_date,
                     int state,
                     str error)
        @return: request info
        '''
        
        request = self.try_get(request_id)
        if request is None:
            message = _('Request ID [{0}] is invalid.')
            raise InvalidRequestIDException(message.format(request_id))
        return request
        
    def set_completed(self, request_id, **options):
        '''
        Completes the state of the given request.
        
        @param str request_id: request ID
        @param request_id: request ID
        '''
        
        self._update_request(request_id, state=TransactionCoordinator.StateEnum.COMPLETED)
        
    def set_failed(self, request_id, error, **options):
        '''
        Sets the state of the given request to failed.
        
        @param str request_id: request ID
        @param str error: error description 
        '''
        
        self._update_request(request_id, 
                             state=TransactionCoordinator.StateEnum.FAILED, 
                             error=error)
        
    def get_transaction(self, transaction_id, **options):
        '''
        Returns transaction information.
        
        @param str transaction_id: transaction ID
        
        @rtype: dict(str id,
                     datetime creation_date,
                     str channel_id,
                     str user_name)
        @return: transaction data
        '''
        
        transaction = self._try_get_transaction(transaction_id)
        if transaction is None:
            raise RequestRecordManagerException('Could not find transaction [{0}] '.format(transaction_id))
        return transaction

    def get_transaction_detail(self, transaction_id, **options):
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
        
        transaction = self.get_transaction(transaction_id)
        transaction.requests = []
        for request_id in self._requests:
            request = self._requests[request_id]
            if request.transaction_id == transaction_id:
                transaction.requests.append(request)
        return request
            
    def get_request_state(self, request_id):
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
        
        return self.get(request_id).state
    