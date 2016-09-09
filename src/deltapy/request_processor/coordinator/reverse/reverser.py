'''
Created on Jan 17, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class Reverser(DeltaObject):
    '''
    It defines algorithm of reversing an action.     
    '''
    
    def reverse(self, params, **options):
        '''
        Reverses an action using the given parameters.
        
        @param params: required parameters to reverse
        '''

        raise NotImplementedError()
