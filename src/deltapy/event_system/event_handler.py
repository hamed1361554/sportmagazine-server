'''
Created on Apr 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.core import DeltaObject


class DeltaEventHandler(DeltaObject):
    '''
    Event handler class.
    '''
    
    def __init__(self, name):
        DeltaObject.__init__(self)
        self._enabled = True
        self._set_name_(name)
        
    def set_enable(self, enable):
        '''
        Sets enable or disable this handler.
        @param enable: enable flag.
        '''
        self._enabled = enable
        
    def is_enable(self):
        '''
        Returns enable status of this handler.
        '''
        return self._enabled
    
    def before(self, params):
        '''
        It will called before specified function which 
        is event point to, executed. 
        @param params: this parameter included event, 
        pointed function and it's parameters. 
        '''
        
    def after(self, params):
        '''
        It will called before specified function which 
        is event point to, executed. 
        @param params: this parameter included event, pointed function, 
        it's parameters and it's result. 
        '''

class DeltaFunctionEventHandler(DeltaEventHandler):
    '''
    '''
    
    def __init__(self, name, before, after):
        DeltaEventHandler.__init__(self, name)
        self._before = before
        self._after = after
        
    def before(self, params):
        '''
        It will called before specified function which 
        is event point to, executed. 
        @param params: this parameter included event, 
        pointed function and it's parameters. 
        '''
        if self._before is not None:
            return self._before(params)
        
    def after(self, params):
        '''
        It will called before specified function which 
        is event point to, executed. 
        @param params: this parameter included event, pointed function, 
        it's parameters and it's result. 
        '''

        if self._after is not None:
            return self._after(params)

        
        
        