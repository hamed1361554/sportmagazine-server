'''
Created on Nov 7, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.services import get_component
from deltapy.locals import APP_BATCH

def get_process_units(status = None):
    '''
    Returns all process units by the given status
    
    @param status: status
        'Stopped'
        'InProgress'
        'Suspended'
        'Completed'
        'Ready'
        'NotReady'
        'Failed'
    @return: [ProcessUnit]
    '''
    
    return get_component(APP_BATCH).get_process_units(status)
    
def get_process_unit(name):
    '''
    Returns specefic process unit.
    
    @param name: name of process unit.
    @return: ProcessUnit
    '''
    
    return get_component(APP_BATCH).get_process_unit(name)
    
def add_process_unit(process_unit, **options):
    '''
    Adds a process unit to batch processor.
    If a process unit with the same ID exists,
    it will override it.    
    
    @param process_unit: process unit instance
    '''
    
    return get_component(APP_BATCH).add_process_unit(process_unit, **options)

def start(process_unit_name, 
          **options):
    '''
    Starts a process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).start(process_unit_name, 
                                          **options)
   
def join(process_unit_name):
    '''
    Joins to a process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).join(process_unit_name)

def join_to_group(name):
    '''
    Joins to a group of process units.
    
    @param name: process units group
    '''
    
    return get_component(APP_BATCH).join_to_group(name)
    
def resize(process_unit_name, thread_count):
    '''
    Resizes thread count of a process unit.
    
    @param process_unit_name: process unit namr
    @param thread_count: thread count
    '''
    
    return get_component(APP_BATCH).resize(process_unit_name, 
                                           thread_count)
    
def stop(process_unit_name):
    '''
    Stops the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).stop(process_unit_name)
    
def suspend(process_unit_name):
    '''
    Suspends the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).suspend(process_unit_name)
    
def resume(process_unit_name):
    '''
    Resumes the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).resume(process_unit_name)

def get_status(process_unit_name):
    '''
    Returns process unit status.
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).get_status(process_unit_name)

def is_completed(process_unit_name):
    '''
    Returns True if the process unit is completed, otherwise False
    
    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).is_completed(process_unit_name)

def get_process_unit_info(process_unit_name):
    '''
    Returns process unit information.
    
    @param process_unit_name: process unit name
    @return: DynamicObject
    '''
    
    return get_component(APP_BATCH).get_process_unit_info(process_unit_name)

def get_process_unit_performance(process_unit_name):
    '''
    
    @param process_unit_name: process unit name
    @return: float
    '''
    
    return get_component(APP_BATCH).get_process_unit_performance(process_unit_name)

def query_messages(process_unit_name, **filters):
    '''
    Queries on process unit messages.
    
    @param process_unit_name: process unit name
    @param **filters: 
        levels : a list including ERROR, INFO, WARNING
        from_date : from date
        to_date : to date
        contains : text, %text, text%, %text%
        limit: limit of messages that should be return.
        from_serial: serial of message 
        
    @return: [DynamicObject<message_time, name, level, message>]
    '''
    
    return get_component(APP_BATCH).query_messages(process_unit_name, **filters)

def get_last_error(process_unit_name):
    '''
    Returns last error which is written.
    
    @param process_unit_name: process unit name
    @return: str
    '''
    
    return get_component(APP_BATCH).get_last_error(process_unit_name)

def truncate_messages(process_unit_name):
    '''
    Truncates message stream.

    @param process_unit_name: process unit name
    '''
    
    return get_component(APP_BATCH).truncate_messages(process_unit_name)

def get_joined_groups(process_unit_name):
    '''
    Returns the groups which the process unit should be waited for.
    
    @param process_unit_name: process unit name
    @return: []
    '''
    
    return get_component(APP_BATCH).get_joined_groups(process_unit_name)
    
def get_joined_units(process_unit_name):
    '''
    Returns the units which the process unit should be waited for.
    
    @param process_unit_name: process unit name
    @return: []
    '''

    return get_component(APP_BATCH).get_joined_units(process_unit_name)

def get_default_settings(process_unit_name):
    '''
    Returns default settings of given process unit.
    
    @param process_unit_name: process unit name
    @return: DynamicObject
    '''

    return get_component(APP_BATCH).get_default_settings(process_unit_name)
