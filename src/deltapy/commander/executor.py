'''
Created on Oct 20, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class CommandExecutor(DeltaObject): 
    '''
    
    '''
    def execute(self, command, *args, **kargs):
        '''
        Executes a command by given key.
        
        @param key: command key or command name
        '''
        return command.execute(*args, **kargs)
    