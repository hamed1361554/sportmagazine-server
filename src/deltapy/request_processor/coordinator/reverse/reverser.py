'''
Created on Jan 17, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject


class Reverser(DeltaObject):
    '''
    It defines algorithm of reversing an action.     
    '''

    def __init__(self, key, reverser_function):
        '''

        :param key:
        :param function:
        '''

        DeltaObject.__init__(self)

        self._set_name_(key)
        self._reverser_function = reverser_function
    
    def reverse(self, params, **options):
        '''
        Reverses an action using the given parameters.
        
        @param params: required parameters to reverse
        '''

        self._reverser_function(params, **options)
