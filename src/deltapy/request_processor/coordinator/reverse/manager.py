'''
Created on Jan 17, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException
from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator

import deltapy.request_processor.coordinator.recorder.services as coordinator_recorder_services


class ReverseManagerException(DeltaException):
    '''
    Is raised when reverse manager encounters error.
    '''


class ReverseManager(DeltaObject):
    '''
    Reverse Manager
    '''
    
    def __init__(self):
        '''
        Initializes reverse manager.
        '''

        DeltaObject.__init__(self)
        
        self._reversers = {}
        
    def get_reverser(self, reverser_id):
        '''
        Returns the registered reverser using the given parameters.
        
        @param reverser_id: reverser ID
        
        @rtype: Reverser
        @return: registered reverser instance
        '''
        
        return self._reversers[reverser_id]
    
    def try_get_reverser(self, reverser_id):
        '''
        Returns the registered reverser using the given parameters.
        
        @param reverser_id: reverser ID
        
        @rtype: Reverser
        @return: registered reverser instance
        '''
        
        return self._reversers.get(reverser_id)

    def register_reverser(self, reverser, **options):
        '''
        Registers a reverser.
        
        @param reverser: reverser instance
        '''
        
        self._reversers[reverser.get_name()] = reverser
    
    def reverse_transaction(self, transaction_id, **options):
        '''
        Reverses an action by the specified reverser using the given parameters.
        
        @param str transaction_id: transaction ID
        '''

        transaction = coordinator_recorder_services.get_detail_by_transaction_id(transaction_id)
        for request in reversed(transaction.requests):
            self._reverse_request(request.request_id, request, **options)

    def reverse_request(self, request_id, **options):
        '''
        Reverses an action by the specified reverser using the given parameters.
        
        @param request_id: request ID
        @param params: required parameters to reverse
        '''

        request = coordinator_recorder_services.get_by_request_id(request_id)
        return self._reverse_request(request_id, request, **options)

    def _reverse_request(self, request_id, request, **options):
        '''
        Reverses the given request.
        
        @param request: request instance
        '''

        if request is None:
            raise ReverseManagerException('No data found for given request id [{0}]'.format(request_id))

        if request.state != TransactionCoordinator.StateEnum.COMPLETED:
            message = \
                'Request with id [{0}] is in state [{1}]'.format(request_id,
                                                                 TransactionCoordinator.StateEnum.str(request.state))
            raise ReverseManagerException(message)

        reverser = self.try_get_reverser(request.service_id)
        if reverser is None:
            raise ReverseManagerException('No reverser found for service key [{0}]'.format(request.service_id))

        reverser.reverse(request, **options)
        coordinator_recorder_services.update_request_state(request_id,
                                                           TransactionCoordinator.StateEnum.REVERSED)
