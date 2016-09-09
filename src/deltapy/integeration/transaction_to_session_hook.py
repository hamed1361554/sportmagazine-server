'''
Created on Nov 7, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from threading import currentThread 

from deltapy.security.session.hook import SessionHook

class TransactionCleanupHook(SessionHook):
    '''
    '''
    
    def cleanup(self, session):
        '''
        @param session:
        '''

        current_thread = currentThread()
        if hasattr(current_thread, 'transaction_manager'):
            transaction_manager = getattr(current_thread, 'transaction_manager')
            transaction_manager.cleanup()
            delattr(current_thread, 'transaction_manager')
            