'''
Created on Mar 4, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class UniqueIDGenerator(DeltaObject):
    '''
    Base class of unique ID generators.
    '''
    
    def get(self, **options):
        '''
        Returns an unique ID by given options
        
        @param **options: custom parameters
        @return: object 
        '''
        
        raise NotImplementedError()
    
    def put(self, id, **options): 
        '''
        Puts the given ID in queue.
        
        @param id: particular ID
        @param **options:
        '''

        raise NotImplementedError()
    
    def reserve(self, id, **options): 
        '''
        Reserves the given ID.
        
        @param id: particular ID
        @param **options:
        '''

        raise NotImplementedError()

    def refresh(self, **options):
        '''
        Refreshes the unique ID generator by given options
        
        @param **options: custom parameters
        '''
        
        pass
