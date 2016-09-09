'''
Created on Jan 17, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DynamicObject
from deltapy.request_processor.coordinator.coordinator import TransactionCoordinator
import deltapy.request_processor.coordinator.services as coordinator_services

class ReverseManager(DeltaObject):
    '''
    '''
    
    def __init__(self):
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

        transaction = self.get_transaction_detail(transaction_id)
        if transaction.state != TransactionCoordinator.StateEnum.REVERSED:
            for request in reversed(transaction.requests):
                if request.state != TransactionCoordinator.StateEnum.REVERSED:
                    self._reverse_request(request)

    def reverse_request(self, request_id, **options):
        '''
        Reverses an action by the specified reverser using the given parameters.
        
        @param reverser_id: reverser ID
        @param params: required parameters to reverse
        '''

        request = None
        return self._reverse_request(request)

    def _reverse_request(self, request, **options):
        '''
        Reverses the given request.
        
        @param request: request instance
        '''

        params = DynamicObject(input = request.input,
                               result = request.result)
        
        try:        
            reverser = self.get_reverser(request.service_id)
            params = DynamicObject(request.input,
                                   request.result)
            reverser.reverse(params, **options) 
            coordinator_services.update_request_state(request.id, TransactionCoordinator.StateEnum.REVERSED)
        except Exception as error:
            coordinator_services.update_request_state(request.id, TransactionCoordinator.StateEnum.REVERE_FAILED, error = error)
            
