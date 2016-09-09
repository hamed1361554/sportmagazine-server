'''
Created on Apr 7, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.event_system.event import DeltaEvent


class DeltaEventManagerException(DeltaException):
    '''
    Delta event manager exception.
    '''

class DeltaEventManager(DeltaObject):
    '''
    Delta event manager class.
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        self._events = {}
        self._event_handlers_queue = {}
    
    def register_event(self, event_name, event_func):    
        '''
        Registers a new event.
        @param event_name: event name
        '''

        event = DeltaEvent(event_name, event_func)
        self._events[event_name] = event
        
    def get_event(self, event_name):
        event = self._events.get(event_name)
        return event
    
    def get_events(self):
        '''
        Returns all registered events.
        '''
        
        results = []
        for event in self._events.values():
            event_hanlders = event.get_handlers()
            handlers = []
            for event_hanlder in event_hanlders:
                handlers.append(DynamicObject(name = event_hanlder.get_name(),
                                              enable = event_hanlder.is_enable()))
            results.append(DynamicObject(name = event.get_name(),
                                         enable = event.is_enable(),
                                         handlers = handlers))
        return results
    
    def fire(self, event_name, *args, **kwargs):
        '''
        Fires specified event using given parameters. 
        @param event_name: event name
        '''

        if len(self._event_handlers_queue) > 0:
            _missed_events = {}
            for e in self._event_handlers_queue:                
                handlers = self._event_handlers_queue[e]
                event = self.get_event(e)
                if event is None:
                    #raise DeltaEventManagerException('Event[%s] not found.' % e)
                    _missed_events[e] = handlers
                else:
                    for handler in handlers:
                        event.add_handler(handler)

            self._event_handlers_queue = _missed_events

        event = self.get_event(event_name)
        if event is None:
            raise DeltaEventManagerException('Event[%s] not found.' % event_name)

        return event.fire(*args, **kwargs)


    def set_enable(self, event_name, enable):
        '''
        Sets event enable or disable.
        @param event_name: event name
        @param enable: enable flag.
        '''
        event = self.get_event(event_name)
        if event is None:
            raise DeltaEventManagerException('Event[%s] not found.' % event_name)        
        event.set_enable(enable)
        
    def reset_event(self, event_name):
        '''
        Resets specified event.
        @param event_name: event name.
        '''
        
        event = self.get_event(event_name)
        if event is None:
            raise DeltaEventManagerException('Event[%s] not found.' % event_name)       
        event.reset()
        
    def add_event_handler(self, event_name, handler):
        '''
        Adds a new event handler.
        @param event_name: event name.
        @param handler: event handler.
        '''

        #if self._event_handlers_queue.has_key(event_name):
        #    self._event_handlers_queue[event_name].append(handler)
        #else:
        #    self._event_handlers_queue[event_name] = [handler]
        
        event = self.get_event(event_name)
        if event is None:
            raise DeltaEventManagerException('Event[%s] not found.' % event_name)
        event.add_handler(handler)

    def add_event_handler_at(self, event_name, handler, index):
        '''
        Adds a new event handler.
        @param event_name: event name.
        @param handler: event handler.
        '''        
        if self._event_handlers_queue.has_key(event_name):
            self._event_handlers_queue[event_name].insert(index, handler)
        else:
            self._event_handlers_queue[event_name] = [handler]

        #event = self.get_event(event_name)
        #if event is None:
        #    raise DeltaEventManagerException('Event[%s] not found.' % event_name)        
        #event.insert_handler(handler, index)
    
