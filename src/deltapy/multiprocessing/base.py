'''
Created on Feb 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.core import DeltaObject

class BasePool(DeltaObject):
    '''
    Base pool
    '''
    
    def __init__(self, name, size, **options):
        DeltaObject.__init__(self)
        self._set_name_(name)
        self._options = options

        self.__size = 0
        self.set_size(size)
    
    def get_options(self):   
        '''
        Returns pool options
        '''
        return self._options
    
    def set_size(self, size):
        '''
        Sets pool size.

        @param int size: pool size
        '''

        old_size = self.get_size()

        if old_size != size:
            self.__size = size
            self._change_size_(old_size, size)

    def get_size(self):
        '''
        Gets pool size.

        @rtype: int
        @return: pool size
        '''

        return self.__size
        
    def execute(self, func, *args, **kwargs):
        '''
        Executes given function with passed arguments.
        
        @param func: function
        @param args: function arguments
        @param kwargs: function keyword arguments        
        '''
        
    def _change_size_(self, old_size, size):
        '''
        It will be called when pool size is changed.
        @param old_size: previous pool size
        @param size: new pool size
        '''
        raise NotImplementedError()

    def terminate(self):
        '''
        Terminates all workers in pool.
        '''
        raise NotImplementedError()

    def join(self):
        '''
        Joins to all workers in pool.
        '''
        raise NotImplementedError()
    