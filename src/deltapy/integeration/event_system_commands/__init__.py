'''
Created on Apr 7, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.commander.decorators import command
import deltapy.event_system.services as event_system

@command('events.get')
def get_event(event_name):
    '''
    Returns specified event.
    @param event_name: event name.
    '''
    return event_system.get_event(event_name)

@command('events.all')
def get_events():
    '''
    Returns all registered events.
    '''    
    return event_system.get_events()

@command('events.fire')
def fire(event_name, *args, **kwargs):
    '''
    Fires specified event using given parameters. 
    @param event_name: event name
    '''
    return event_system.fire(event_name, *args, **kwargs)

@command('events.enable')
def set_enable(event_name, enable):
    '''
    Sets event enable or disable.
    @param event_name: event name
    @param enable: enable flag.
    '''
    return event_system.set_enable(event_name, enable)

@command('events.reset')    
def reset_event(event_name):
    '''
    Resets specified event.
    @param event_name: event name.
    '''
    return event_system.reset_event(event_name)