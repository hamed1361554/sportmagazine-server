'''
Created on Mar 4, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import uuid

from deltapy.unique_id.generator import UniqueIDGenerator

class UUIDGenerator(UniqueIDGenerator):
    '''
    '''
    
    def get(self, **options):
        '''
        Returns an unique ID by given options
        
        @param **options: custom parameters
        @return: object 
        '''
        
        return str(uuid.uuid4())
    
    def refresh(self, **options):
        '''
        Refreshes the unique ID generator by given options
        
        @param **options: custom parameters
        '''
        
        pass
