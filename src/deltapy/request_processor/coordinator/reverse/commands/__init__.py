'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.request_processor.coordinator.reverse.services as reverse_services


@command('request_processor.coordinator.reverse.reverse_transaction',
         recorder_type='full_recorder')
def reverse_transaction(transaction_id, **options):
    '''
    Reverses an action by the specified reverser using the given parameters.

    @param str transaction_id: transaction ID
    '''

    return reverse_services.reverse_transaction(transaction_id, **options)

@command('request_processor.coordinator.reverse.reverse_request',
         recorder_type='full_recorder')
def reverse_request(request_id, **options):
    '''
    Reverses an action by the specified reverser using the given parameters.

    @param str request_id: request ID
    '''

    return reverse_services.reverse_request(request_id, **options)