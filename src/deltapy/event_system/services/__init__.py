'''
Created on Apr 7, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.event_system import EVENT_MANAGER
from deltapy.application.services import get_component

def register_event(event_name, event_func):    
    '''
    Registers a new event.
    @param event_name: event name
    '''
    
    return get_component(EVENT_MANAGER).register_event(event_name, event_func)

def get_event(event_name):
    '''
    Returns specified event.
    @param event_name: event name.
    '''
    return get_component(EVENT_MANAGER).get_event(event_name)

def get_events():
    '''
    Returns all registered events.
    '''    
    return get_component(EVENT_MANAGER).get_events()

def fire(event_name, *args, **kwargs):
    '''
    Fires specified event using given parameters. 
    @param event_name: event name
    '''
    return get_component(EVENT_MANAGER).fire(event_name, *args, **kwargs)

def set_enable(event_name, enable):
    '''
    Sets event enable or disable.
    @param event_name: event name
    @param enable: enable flag.
    '''
    return get_component(EVENT_MANAGER).set_enable(event_name, enable)
    
def reset_event(event_name):
    '''
    Resets specified event.
    @param event_name: event name.
    '''
    return get_component(EVENT_MANAGER).reset_event(event_name)
    
def add_event_handler(event_name, handler):
    '''
    Adds a new event handler.
    @param event_name: event name.
    @param handler: event handler.
    '''        
    return get_component(EVENT_MANAGER).add_event_handler(event_name, handler)

def add_event_handler_at(event_name, handler, index):
    '''
    Adds a new event handler.
    @param event_name: event name.
    @param handler: event handler.
    '''        
    return get_component(EVENT_MANAGER).add_event_handler_at(event_name, handler, index)
