'''
Performs some utilities for concurrent programming. 
'''

from threading import Thread
from threading import Lock
from threading import Event
import time

class Executor(Thread):
    '''
    A wrapper class for executing the target function in a new thread.
    '''
    def __init__(self, func, delay, callback, *args, **kargs):
        Thread.__init__(self)
        self.__func = func
        self.__callback = callback
        self.__delay = delay
        self.args = args
        self.kargs = kargs

    def run(self):
        '''
        Run method of Thread class.
        '''
        if self.__delay:
            time.sleep(self.__delay)
        result = self.__func(*self.args, **self.kargs)
        if self.__callback:
            self.__callback(result, *self.args, **self.kargs)

def run_in_thread(func, *args, **kargs):
    '''
    Runs the function in a new thread.
    
    @param func: target function
    @return: Thread
    '''
    executor = Executor(func, None, None, *args, **kargs)
    executor.start()
    return executor

class ConflictController:
    '''
    Controls conflict of lists items.
    '''
    
    def __init__(self):
        self._active_lists = {}
        self._lock = Lock()
        
    def _add_to_queue_(self, lst):
        try:
            self._lock.acquire()
            
            obj_set, obj_event = self._get_conflicted_list_(lst)
            if obj_event:
                return obj_event
            
            event = Event()
            event.clear()
            self._active_lists[id(lst)] = set(lst), event
            
            return None
        finally:
            self._lock.release()
    
    def _remove_from_queue_(self, activation_id):
        try:
            self._lock.acquire()
            if activation_id in self._active_lists:
                obj_set, event = self._active_lists.pop(activation_id)
                event.set()
                del obj_set
                del event
        finally:
            self._lock.release()
            
    def _get_conflicted_list_(self, lst):
        current_set = set(lst)
        for obj_set, event in self._active_lists.values():
            if len(current_set.intersection(obj_set)) > 0:
                return obj_set, event
        return None, None
    
    def has_conflict(self, lst):
        '''
        Returns True if some list items exists in other lists.
        '''
        
        obj_set, obj_event = self._get_conflicted_list_(lst) 
        
        return obj_set is None
        
    def activate(self, lst):
        '''
        Adds a list in queue.
        
        @param lst: list object
        '''
        
        while True:
            event = self._add_to_queue_(lst)
            if event:
                event.wait()
            else:
                return id(lst)
    
    def deactivate(self, activation_id):
        '''
        Removes a list from queue.
        
        @param lst: list object
        '''
        
        self._remove_from_queue_(activation_id)
    
class LockedArea:
    def __init__(self, lock):
        self._lock = lock
    
    def __enter__(self, *args):
        self._lock.acquire()
        
    def __exit__(self, *args):
        self._lock.release()
    
