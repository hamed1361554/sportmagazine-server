'''
Created on May 18, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import threading

def thread_stop_func():
    '''
    The function wraps the Thread class __stop function.
    '''
    
    __old_stop = threading.Thread._Thread__stop
    
    def __stop(self):
        '''
        Overrides the __stop function of Thread class 
        '''
        
        if hasattr(self, 'transaction_manager'):
            current_transaction_manager = getattr(self, 'transaction_manager')
            
            if current_transaction_manager:
                current_transaction_manager.cleanup()
                setattr(self, 'transaction_manager', None)
                del current_transaction_manager
                
        return __old_stop(self)
    
    return __stop

def thread_start_func():
    '''
    The function wraps the Thread class __start function.
    '''
    
    __old_start = threading.Thread.start
    
    def start(self):
        '''
        Overrides the start function of Thread class 
        '''
        
        current_thread = threading.currentThread()
        
        if hasattr(current_thread, 'session'):
            
            # Getting the session object of this thread...
            current_session = getattr(current_thread, 'session')
            setattr(self, 'session', current_session)

        return __old_start(self)
    
    return start

def boot():
    # Wrapping old function...
    threading.Thread._Thread__stop = thread_stop_func()
    threading.Thread.start = thread_start_func()
