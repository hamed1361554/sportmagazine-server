'''
Created on Mar 4, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
import uuid

from deltapy.unique_id.generator import UniqueIDGenerator


class UUIDGenerator(UniqueIDGenerator):
    '''
    UUID generator
    '''

    def __init__(self):
        '''
        Initialzes uuid generator.
        '''

        UniqueIDGenerator.__init__(self)
        self.__custom_node = uuid.getnode() - os.getpid()
    
    def get(self, **options):
        '''
        Returns an unique ID by given options
        
        @param **options: custom parameters
        @return: object 
        '''

        # Protocol 4 is as unique as underlying random generator,
        # which is not random enough for most of times.
        # return str(uuid.uuid4())

        # We have to use protocol one which is based on time and
        # current machine's mac address. We combine it with pid of
        # current process, to make it even more unique.
        return str(uuid.uuid1(node=self.__custom_node))
    
    def refresh(self, **options):
        '''
        Refreshes the unique ID generator by given options
        
        @param **options: custom parameters
        '''
        
        pass
