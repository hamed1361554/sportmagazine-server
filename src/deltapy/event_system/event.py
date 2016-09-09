'''
Created on Apr 7, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject


class DeltaEvent(DeltaObject):
    '''
    Delta event class.
    '''
    
    def __init__(self, name, function):
        DeltaObject.__init__(self)
        self._set_name_(name)
        self._enabled = True
        self._handlers = []
        self._function = function
    
    def set_enable(self, enable):
        '''
        Sets event enable or disable.
        @param enable: enable flag.
        '''
        self._enabled = enable
        
    def is_enable(self):
        '''
        Returns enable flag of this event.
        '''
        return self._enabled

    def fire(self, *args, **kwargs):
        '''
        fires the event.
        '''
        
        if self._enabled:
            params = {}
            params['event'] = self
            params['function'] = self._function
            params['args'] = args
            params['kwargs'] = kwargs
            
            reversed_handlers = []
            
            for handler in self._handlers:
                handler.before(params)
                reversed_handlers.insert(0, handler)
        
        params['result'] = self._function(*args, **kwargs)      
        
        if self._enabled:            
            for handler in reversed_handlers:
                handler.after(params)
        
        return params['result']
            
    def insert_handler(self, handler, index):
        '''
        Adds a new handler at specified index.
        @param handler: event handler function.
        @param index: index of handler
        '''
        self._handlers.insert(index, handler)
            
    def add_handler(self, handler):
        '''
        Adds a new handler at specified index.
        @param handler: event handler function.
        '''
        self._handlers.append(handler)
    

    def get_handlers(self):
        '''
        Returns all registered handlers.
        '''
        
        return iter(self._handlers)                
    
    def get_handler(self, name):
        '''
        Removes specified handler.
        
        @param name: handler name
        '''
        
        for handler in self._handlers:
            if handler.get_name() == name:
                return handler

    def remove_handler(self, name):
        '''
        Removes specified handler.
        
        @param name: handler name
        '''
        
        handler = self.get_handler(name) 
        if handler is not None:
            self._handlers.remove(handler)                
    
    def reset(self):
        '''
        Resets registered handles.
        '''
        self._handlers = []
    
    