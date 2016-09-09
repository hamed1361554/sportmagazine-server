'''
Created on Jun 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from Queue import Queue
from threading import Lock

class ObjectPool(object):
    
    DEFAULT = 'default'

    def __init__(self, 
                 name, 
                 min, 
                 max, 
                 growup,
                 **options):
        self._name = name
        self.__pool = Queue()
        self.__busy = {}
        self.__lock = Lock()
        self.__min = min
        self.__max = max
        self.__growup = growup
        self.__options = options
        if self.__min > 0:
            self._growup_(self.__min)
            
    def get_options(self):
        '''
        Returns options.
        
        @return: str
        '''
        
        return self._options
            
    def get_name(self):
        '''
        Returns pool name.
        
        @return: str
        '''
        return self._name
        
    def _create_object_(self):
        '''
        Creates a new object
        
        @return: object
        '''
        
        raise NotImplementedError()

    def _destroy_object_(self, object):
        '''
        Destroys object.
        
        @param object: object instance
        '''
        
        raise NotImplementedError()

    def _acquire_(self):
        '''
        Acquires an object from pool.
        
        @return: object
        '''

        if self.__pool.qsize() == 0:
            self._growup_(self.__growup)
        object = None
        if self.__pool.qsize() == 0:
            object = self._create_object_()
        else:
            object = self.__pool.get_nowait()
            if not self._is_object_alive_(object):
                self._destroy_object_(object)
                return self._acquire_()
        self.__busy[object] = object
        return object
            
    def acquire(self):
        '''
        Acquires an object from pool.
        
        @return: object
        '''

        try:
            self.__lock.acquire()
            
            return self._acquire_()
        finally:
            self.__lock.release()

    def _growup_(self, size):
        '''
        Grows up object pool.
        
        @return: object
        '''

        for i in xrange(size):
            if self.__max > self.__pool.qsize():
                break
            object = self._create_object_()
            self.__pool.put(object)
            
    def _is_object_alive_(self, object):            
        '''
        Return True if object is alive.
        
        @param object: object object
        @return: bool
        '''
        
        raise NotImplementedError()
        
    def release(self, object):
        '''
        Releases object.
        
        @param object: object instance
        '''
        try:
            self.__lock.acquire()
            busy_object = self.__busy.pop(object)
            if self.__pool.qsize() >= self.__max:
                self._destroy_object_(object)
            else:
                self.__pool.put(busy_object)
        finally:
            self.__lock.release()

    def resize(self, min, max, growup):
        '''
        Resizes object pool.
        
        @param min: pool minimum size
        @param max: pool maximum size
        @param growup: pool grow up
        '''
        try:
            self.__lock.acquire()
            self.__min = min
            self.__max = max
            if self.__min > self.__max:
                raise Exception('Invalid range: minimum is bigger than maximum.')
            if self.__min < 0 or self.__max < 0:
                raise Exception('Invalid range: minimum or maximum is less than zero.')
            self.__growup = growup
        finally:
            self.__lock.release()
            
    def __str__(self):
        return "%s" % self.get_name()
