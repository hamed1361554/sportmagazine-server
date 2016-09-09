'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.request_processor.coordinator.reverse import APP_REVERSE_MANAGER


def get_reverser(reverser_id):
    '''
    Returns the registered reverser using the given parameters.
    
    @param reverser_id: reverser ID
    
    @rtype: Reverser
    @return: registered reverser instance
    '''
    
    return get_component(APP_REVERSE_MANAGER).get_reverser(reverser_id)

def try_get_reverser(reverser_id):
    '''
    Returns the registered reverser using the given parameters.
    
    @param reverser_id: reverser ID
    
    @rtype: Reverser
    @return: registered reverser instance
    '''
    
    return get_component(APP_REVERSE_MANAGER).try_get_reverser(reverser_id)

def register_reverser(reverser, **options):
    '''
    Registers a reverser.
    
    @param reverser: reverser instance
    '''
    
    return get_component(APP_REVERSE_MANAGER).register_reverser(reverser, **options)
    
def reverse(reverser_id, params, **options):
    '''
    Reverses an action by the specified reverser using the given parameters.
    
    @param reverser_id: reverser ID
    @param params: required parameters to reverse
    '''

    return get_component(APP_REVERSE_MANAGER).reverse(reverser_id, params, **options)
