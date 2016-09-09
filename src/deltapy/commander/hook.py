'''
Created on Oct 21, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class CommandExecutionHook(DeltaObject):
    def __init__(self):
        DeltaObject.__init__(self)
        
        self.__enable = True
        
    def set_enable(self, flag):
        '''
        Enables or disable the hook.
        
        @param flag: enable flag
        '''
        
        self.__enable = flag
        
    def is_enable(self):
        '''
        Returns True if the hook is enable.
        
        @return: boolean
        '''
        return self.__enable
    
    def before_execute(self, commander, command, *args, **kargs):
        '''
        This method will be called before command execution.
        
        @param commander: commander
        @param command: command
        '''
        pass
    
    def after_execute(self, commander, command, result, *args, **kargs):
        '''
        This method will be called after command execution.
        
        @param commander: commander
        @param command: command
        @param result: command execution result
        '''
        pass
    
    def exception(self, commander, command, error, *args, **kargs):
        '''
        This method will be called whenever an exception occurred during executing a command.
        
        @param commander: commander
        @param command: command
        @param error: exception instance
        '''
