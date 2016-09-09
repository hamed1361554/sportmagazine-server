'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.unique_id.services as unique_id 

@command('unique_id.get')
def get_id(generator_name, **options):
    '''
    Returns an unique ID using corresponded registered generator.
    
    @param generator_name: unique ID generator name.
    @param **options: unique ID generator options
    @return: object
    '''
    
    return unique_id.get_id(generator_name, **options)

@command('unique_id.refresh')
def refresh(generator_name, **options):
    '''
    Refreshes the unique ID generator. 
    
    @param generator_name: unique ID generator name.
    @param **options: unique ID generator options
    '''
    
    return unique_id.refresh(generator_name, **options)

@command('unique_id.put')
def put_id(generator_name, id, **options): 
    '''
    Puts the given ID in queue.
    
    @param generator_name: unique ID generator name.
    @param id: particular ID
    @param **options:
    '''

    return unique_id.put_id(generator_name, id, **options)

@command('unique_id.reserve')
def reserve_id(generator_name, id, **options): 
    '''
    Reserves the given ID.
    
    @param generator_name: unique ID generator name.
    @param id: particular ID
    @param **options:
    '''
    
    return unique_id.reserve_id(generator_name, id, **options)
