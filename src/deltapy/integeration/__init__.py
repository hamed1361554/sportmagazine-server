'''
Created on Nov 7, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package 
import deltapy.security.session.services as session_services

class IntegerationPackage(Package):
    '''
    Integeration package.
    '''
    
    __depends__ = ['deltapy.config', 
                   'deltapy.logging', 
                   'deltapy.commander', 
                   'deltapy.security', 
                   'deltapy.transaction']
    
    def load(self):
        Package.load(self)
        
        from deltapy.integeration.transaction_to_session_hook import TransactionCleanupHook 
        
        session_services.add_hook(TransactionCleanupHook())
