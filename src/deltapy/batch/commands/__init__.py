'''
Created on Nov 7, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.batch.services as batch
from deltapy.core import DynamicObject
from deltapy.event_system.decorators import delta_event


@command('batch.all')
def get_process_units():
    '''
    Returns all process units.
    
    @return: [ProcessUnit]
    '''
    
    units = []
    for unit in batch.get_process_units():
        units.append(batch.get_process_unit_info(unit.get_name()))
    return units
    
@command('batch.list')
def list_process_units(status = None):
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
    
    units = []
    for unit in batch.get_process_units(status):
        units.append(batch.get_process_unit_info(unit.get_name()))
    return units

@command('batch.get')
def get_process_unit(process_unit_name):
    '''
    Returns specefic process unit.
    
    @param name: name of process unit.
    @return: ProcessUnit
    '''
    
    return batch.get_process_unit_info(process_unit_name)

    
@command('batch.start')
@delta_event('command.batch.start')
def start(process_unit_name, 
          **options):
    '''
    Starts a process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return batch.start(process_unit_name, 
                       **options)
   
@command('batch.resize')
@delta_event('command.batch.resize')
def resize(process_unit_name, thread_count):
    '''
    Resizes thread count of a process unit.
    
    @param process_unit_name: process unit namr
    @param thread_count: thread count
    '''
    
    return batch.resize(process_unit_name, 
                        thread_count)
    
@command('batch.stop')
@delta_event('command.batch.stop')
def stop(process_unit_name):
    '''
    Stops the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return batch.stop(process_unit_name)
    
@command('batch.suspend')
@delta_event('command.batch.suspend')
def suspend(process_unit_name):
    '''
    Suspends the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return batch.suspend(process_unit_name)
    
@command('batch.resume')
@delta_event('command.batch.resume')
def resume(process_unit_name):
    '''
    Resumes the process unit.
    
    @param process_unit_name: process unit name
    '''
    
    return batch.resume(process_unit_name)

@command('batch.status')
def get_status(process_unit_name):
    '''
    Returns process unit status.
    
    @param process_unit_name: process unit name
    '''
    
    return batch.get_status(process_unit_name)

@command('batch.is_completed')
def is_completed(process_unit_name):
    '''
    Returns True if the process unit is completed, otherwise False
    
    @param process_unit_name: process unit name
    '''
    
    return batch.is_completed(process_unit_name)

@command('batch.performance')
def get_process_unit_performance(process_unit_name):
    '''
    
    @param process_unit_name: process unit name
    @return: float
    '''
    
    return batch.get_process_unit_performance(process_unit_name)

@command('batch.query_messages')
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
    
    return batch.query_messages(process_unit_name, **filters)

@command('batch.last_error')
def get_last_error(process_unit_name):
    '''
    Returns last error which is written.
    
    @param process_unit_name: process unit name
    @return: str
    '''
    
    return batch.get_last_error(process_unit_name)

@command('batch.truncate_messages')
def truncate_messages(process_unit_name):
    '''
    Truncates message stream.

    @param process_unit_name: process unit name
    '''
    
    return batch.truncate_messages(process_unit_name)

@command('batch.joined_groups')
def get_joined_groups(process_unit_name):
    '''
    Returns the groups which the process unit should be waited for.
    
    @param process_unit_name: process unit name
    @return: []
    '''
    
    return batch.get_joined_groups(process_unit_name)
    
@command('batch.joined_units')
def get_joined_units(process_unit_name):
    '''
    Returns the units which the process unit should be waited for.
    
    @param process_unit_name: process unit name
    @return: []
    '''

    return batch.get_joined_units(process_unit_name)

@command('batch.defaults')
def get_default_settings(process_unit_name):
    '''
    Returns default settings of given process unit.
    
    @param process_unit_name: process unit name
    @return: DynamicObject
    '''

    return batch.get_default_settings(process_unit_name)