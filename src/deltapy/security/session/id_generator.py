'''
Created on May 19, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import uuid

from deltapy.unique_id.generator import UniqueIDGenerator

class SessionIDGenerator(UniqueIDGenerator):
    '''
    '''
    
    def get(self, **options):
        '''
        Returns an unique ID by given options
        
        @param **options: custom parameters
        @return: object 
        '''
        
        return str(uuid.uuid4())
    