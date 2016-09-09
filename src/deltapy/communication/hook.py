'''
Created on Oct 21, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class CommunicationHook(DeltaObject):
    '''
    Provides hooking on send and receive in communication.
    '''
    
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

    def send(self,
             communicator, 
             listener, 
             result, 
             ip, 
             ticket, 
             user_name, 
             command_key, 
             *args, 
             **kargs):
        pass
    
    def receive(self,
                communicator, 
                listener, 
                ip, 
                ticket, 
                user_name, 
                command_key, 
                *args, 
                **kargs):
        pass

