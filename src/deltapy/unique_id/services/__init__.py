'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.application.services import get_component
from deltapy.unique_id import UNIQUE_ID_MANAGER

def register_generator(name, generator):
    '''
    Registers an unique ID generator.
    
    @param name: generator name
    @param generator: generator instance
    '''
    
    return get_component(UNIQUE_ID_MANAGER).register_generator(name, generator)
    
def get_generator(name):
    '''
    Returns the specific generator by given name.
    
    @param name: generator name
    @return: UniqueIDGenerator
    '''
    
    return get_component(UNIQUE_ID_MANAGER).get_generator(name)

def get_id(generator_name, **options):
    '''
    Returns an unique ID using corresponded registered generator.
    
    @param generator_name: unique ID generator name.
    @param **options: unique ID generator options
    @return: object
    '''
    
    return get_component(UNIQUE_ID_MANAGER).get_id(generator_name, **options)

def put_id(generator_name, id, **options): 
    '''
    Puts the given ID in queue.
    
    @param generator_name: unique ID generator name.
    @param id: particular ID
    @param **options:
    '''

    return get_component(UNIQUE_ID_MANAGER).put_id(generator_name, id, **options)

def reserve_id(generator_name, id, **options): 
    '''
    Reserves the given ID.
    
    @param generator_name: unique ID generator name.
    @param id: particular ID
    @param **options:
    '''
    
    return get_component(UNIQUE_ID_MANAGER).reserve_id(generator_name, id, **options)

def refresh(generator_name, **options):
    '''
    Refreshes the unique ID generator. 
    
    @param generator_name: unique ID generator name.
    @param **options: unique ID generator options
    '''
    
    return get_component(UNIQUE_ID_MANAGER).refresh(generator_name, **options)
