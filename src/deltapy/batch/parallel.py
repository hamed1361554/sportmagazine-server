'''
Created on Sep 1, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.core import DeltaException

import threading
import Queue
import time
import traceback

from deltapy.utils.time_counter import TimeCounter


class DynamicSemaphore:
    '''
    Creates a dynamic (in size) semaphore object.
    '''
    def __init__(self, max_size):
        '''
        class initialization.
        '''
        self._max =  max_size
        self._count = 0
        self._event = threading.Event()
        self._event.set()
        self._lock = threading.Lock()
        self._set_lock = threading.Lock()
        
    def acquire(self):
        '''
        Acquires lock.
        '''
        self._lock.acquire()
        
        if self._count >= self._max - 1:
            self._event.clear()

        self._event.wait()
        self._increment_()
        
        self._lock.release()
        
    def release(self):
        '''
        Releases the lock.
        '''
        self._decrement_()
        if self._count < self._max - 1:
            self._event.set()
        
    def _increment_(self):
        '''
        Increments locks.
        '''
        self._set_lock.acquire()
        self._count += 1
        self._set_lock.release()

    def _decrement_(self):
        '''
        Decrements locks.
        '''
        self._set_lock.acquire()
        self._count -= 1
        self._set_lock.release()
    
    def resize(self, new_max):
        '''
        Resizes semaphore size.
        '''
        self._set_lock.acquire()
        self._max = new_max
        self._set_lock.release()

class ParallelTask(threading.Thread):
    '''
    ParallelTask objects represent activity that is run in a separate thread.
    '''
    def __init__(self, 
                 parallel_executer, 
                 execute_func, 
                 params):
        threading.Thread.__init__(self)
        self._parallel_executer = parallel_executer
        self._execute_func = execute_func
        self._params = params
        self._result = None
        self._exception = None
        
    def run(self):
        '''
        Overrides run method of Thread class
        When a task is started, this code will be executed.
        '''
        try:
            if(self._parallel_executer._before_start_task):
                self._parallel_executer._before_start_task(self._params)
            self._result = self._execute_func(self._params)
            if(self._parallel_executer._after_complete_task):
                self._parallel_executer._after_complete_task(self._params, self._result)
        except Exception, error:
            self._exception = error
            if(self._parallel_executer._on_task_failed):
                self._parallel_executer._on_task_failed(self._params, error)
        self._parallel_executer._release_()
        
    
    
    def get_result(self):
        '''
        Returns the final result of the executed function.
        
        @rtype: object
        '''
        
        return self._result
    
    def get_exception(self):
        '''
        Returns occurred exception during the function execution
        
        @rtype: Exception
        '''
        
        return self._exception


class ParallelExecutorException(DeltaException):
    '''
    Parallel executer exception
    '''
            
class ParallelExecutor(threading.Thread):
    '''
    Creates a objects which could be runs several tasks in parallel mode.
    It is also a thread pool object.
    '''
    
    class StatusEnum:
        '''
        Represents ParallelExecutor object state.
        '''
        
        NOT_READY = 'NotReady'
        PREPROCESSING = 'Preprocessing'
        READY = 'Ready'
        IN_PROGRESS = 'InProgress'
        SUSPENDED = 'Suspended'
        STOPPING = 'Stopping'
        STOPPED = 'Stopped'
        COMPLETED = 'Completed'
        POSTPROCESSING = 'Postprocessing'
        FAILED = 'Failed'
      
    def __init__(self, 
                 name,
                 execute_func, 
                 thread_count = 1):
        threading.Thread.__init__(self)
        self._name = name
        self._queue = Queue.Queue()
        self._execute_func = execute_func
        self._threads = []
        self._event = threading.Event()
        self._event.set()
        self._thread_count = thread_count
        self._time_counter = TimeCounter()
        self._semaphore = None
        self._start_time = None

        self._before_start = None
        self._after_finished = None
        self._before_start_task = None
        self._after_complete_task = None
        self._on_task_failed = None
        self._on_failed = None
        self._status = ParallelExecutor.StatusEnum.NOT_READY
        self._results = None
        self._exceptions = None

    def set_before_start(self, func):
        '''
        Sets the function which will be executed before starting to launch tasks.

        @param func: handler function
        '''
        self._before_start = func
    
    def set_after_finished(self, func):
        '''
        Sets the function which will be executed after all tasks finished.

        @param func: handler function
        '''
        self._after_finished = func
    
    def set_on_failed(self, func):
        '''
        Sets the function which will be executed after all tasks finished.

        @param func: handler function
        '''
        self._on_failed = func

    def set_before_start_task(self, func):
        '''
        Sets the function which will be executed before starting every tasks.

        @param func: handler function
        '''
        self._before_start_task = func
    
    def set_after_complete_task(self, func):
        '''
        Sets the function which will be executed when a task is completed.

        @param func: handler function
        '''
        self._after_complete_task = func
    
    def set_on_task_failed(self, func):
        '''
        Sets the function which will be executed when a task is failed.
        
        @param func: handler function
        '''
        self._on_task_failed = func
        
    def get_name(self):
        '''
        Returns the parallel executor name.
        
        @return: str
        '''
        return self._name
    
    def can_add_parameter(self):
        '''
        Returns True if we can add parameter according to current state.
        
        @return: boolean
        '''
        
        if self._status in (ParallelExecutor.StatusEnum.COMPLETED,
                            ParallelExecutor.StatusEnum.STOPPED,
                            ParallelExecutor.StatusEnum.STOPPING,
                            ParallelExecutor.StatusEnum.FAILED):
            return False
        
        return True
    
    def add_parameter(self, parameter):
        '''
        Adding new parameter to parameters queue.
        '''

        if self.can_add_parameter():
            self._queue.put(parameter)
            self._status = ParallelExecutor.StatusEnum.READY

    def add_parameters(self, parameters):
        '''
        Adding a list of parameters to parameters queue.
        '''
        if self.can_add_parameter():
            for param in parameters:
                self.add_parameter(param)
        
    def run(self):
        '''
        Overrides Thread class's run method.
        It will be executed when parallel executor is started. 
        '''
        self._threads = []
        self._results = []
        self._exceptions = []
        try:
            self._time_counter.start("PreProcess")
            if self._before_start is not None:
                self._status = ParallelExecutor.StatusEnum.PREPROCESSING
                self._before_start()
            self._time_counter.stop("PreProcess")

            if self._status not in (ParallelExecutor.StatusEnum.READY,
                                    ParallelExecutor.StatusEnum.STOPPED):
                if self._status == ParallelExecutor.StatusEnum.STOPPING:
                    self._status = ParallelExecutor.StatusEnum.STOPPED
                    raise Exception('The parallel executor is aborted and [%s].' % self._status)
                else:
                    raise Exception('The parallel executor is [%s].' % self._status)
            
            self._status = ParallelExecutor.StatusEnum.IN_PROGRESS

            self._time_counter.start("Run")
            self._start_time = time.time()
            self._semaphore = DynamicSemaphore(self._thread_count + 1)
            self._threads = []
            while not self._queue.empty() and self._status != ParallelExecutor.StatusEnum.STOPPING:
                self._event.wait()
                self._acquire_()
                params = self._queue.get()
                task = ParallelTask(self, self._execute_func, params)
                self._threads.append(task)
                task.start()

            for thread in self._threads:
                thread.join()
                self._results.append(thread.get_result())
                self._exceptions.append(thread.get_exception())
                      
            self._time_counter.stop("Run")

            if self._status != ParallelExecutor.StatusEnum.STOPPING:
                self._time_counter.start("PostProcess")
                if self._after_finished is not None:
                    self._status = ParallelExecutor.StatusEnum.POSTPROCESSING
                    self._after_finished()
                self._time_counter.stop("PostProcess")
                self._status = ParallelExecutor.StatusEnum.COMPLETED
            else:
                self._status = ParallelExecutor.StatusEnum.STOPPED
                #Calling failed method of process unit.
                if self._on_failed is not None:
                    self._on_failed(None, "Stopped")
                
        
        except Exception, error:
            if self._status not in (ParallelExecutor.StatusEnum.STOPPED):
                self._status = ParallelExecutor.StatusEnum.FAILED
            if self._on_failed:
                self._on_failed(error, traceback.format_exc())

    def get_remained_count(self):
        '''
        Returns remained tasks count.
        
        @return: int
        '''
        return self._queue.qsize()    

    def get_compeleted_count(self):
        '''
        Returns completed tasks count.
        
        @return: int
        '''
        return sum([1 for thread in self._threads if not thread.is_alive()])
        
    def get_running_count(self):
        '''
        Returns tasks count which are running now.
        
        @return: int
        '''
        return sum([1 for thread in self._threads if thread.is_alive()])

    def get_running_times(self):
        '''
        Returns tasks running duration in seconds.
        
        @return: float
        '''
        return self._time_counter.get("Run")    

    def get_preprocess_times(self):
        '''
        Returns tasks pre-processing duration in seconds.
        
        @return: float
        '''
        return self._time_counter.get("PreProcess")    

    def get_postprocess_times(self):
        '''
        Returns tasks pre-processing duration in seconds.
        
        @return: float
        '''
        return self._time_counter.get("PostProcess")    
        
    def wait_for_complete(self):
        '''
        This function waits until all tasks be completed, failed or stopped. 
        '''
        self.join()
        return time.time() - self._start_time

    def reset(self):
        '''
        This function resets parallel executer and also resets parameter queue.
        '''
        self.stop()
        self._queue = Queue.Queue()
    
    def stop(self):
        '''
        Stops remained tasks.
        '''
        if self._status in (ParallelExecutor.StatusEnum.PREPROCESSING,
                            ParallelExecutor.StatusEnum.IN_PROGRESS):
            self._status = ParallelExecutor.StatusEnum.STOPPING
    
    def suspend(self):
        '''
        Suspends all tasks of parallel executer.
        '''
        if self._status == ParallelExecutor.StatusEnum.IN_PROGRESS:
            self._status = ParallelExecutor.StatusEnum.SUSPENDED
            self._event.clear()
        
    def resume(self):
        '''
        Resumes tasks which are suspended.
        '''
        if self._status == ParallelExecutor.StatusEnum.SUSPENDED:
            self._status = ParallelExecutor.StatusEnum.IN_PROGRESS
            self._event.set()
        
    def resize(self, thread_count):
        '''
        Resize parallel thread pool.
        '''
        self._thread_count = thread_count
        self._semaphore.resize(thread_count + 1)
                
    def get_size(self):
        '''
        Returns parallel thread pool size.
        '''
        return self._thread_count
        
    def is_running(self):
        '''
        Returns True if tasks are running.
        '''

        return not self.can_run()
    
    def is_completed(self):
        '''
        Returns True if tasks are completed.
        
        @return: boolean
        '''
        
        return self._status == ParallelExecutor.StatusEnum.COMPLETED
    
    def can_run(self):
        '''
        Define if the current state allows running the executer.
        
        @return: True if can start, otherwise False
        
        @rtype: Boolean
        '''
        
        
        if self._status in (ParallelExecutor.StatusEnum.COMPLETED,
                            ParallelExecutor.StatusEnum.FAILED,
                            ParallelExecutor.StatusEnum.STOPPED,
                            ParallelExecutor.StatusEnum.NOT_READY):
            return True
        
        return False
    
    def _acquire_(self):
        '''
        Acquire semaphore lock.
        '''
        self._semaphore.acquire()
    
    def _release_(self):
        '''
        Releases semaphore lock.
        '''
        self._semaphore.release()
       
    def get_status(self):
        '''
        Returns parallel executor status
        '''
        
        return self._status
    
    def check_fail(self, **options):
        '''
        Checks whether all task are faultlessly finished otherwise will raise an 
        error that consists all of the child errors related to each task.
        
        @keyword exception_class: exception class
        @note: Default value of exception class is ParallelExecutorException.
        
        @keyword show_inner_exception_message: show inner exception message
        @note: Default value of show_inner_exception_message is True.  
        '''

        # Getting exception class
        exception_class = options.get('exception_class')
        if exception_class is None:
            exception_class = ParallelExecutorException
        
        # Determining if inner exception message should be displayed
        show_inner_exception_message = options.get('show_inner_exception_message')
        if show_inner_exception_message is None:
            show_inner_exception_message = True
            
        self.join()
        
        # Getting exceptions
        critical_errors = self.get_exceptions()
        
        if critical_errors is not None:
            # Initializing error message and its inner data
            message = ''
            inner_exception_data = []
            
            # Preparing inner exception data
            for error in critical_errors:
                if error is not None:
                    inner_exception_data.append(error.message)
            
            # Raising exception if errors exist        
            if len(inner_exception_data) > 0:
                # Adding inner exceptions message to error message
                if show_inner_exception_message:
                   for inner_exception in inner_exception_data:
                       message += '\n{inner_exception}'.format(inner_exception=inner_exception)
                
                # Preparing exception
                exception = exception_class(message)
                exception.get_data()['parallel_executer_error'] = \
                    'Executing [{name}] failed'.format(name=self.get_name())
                exception.get_data()['inner_exceptions'] = inner_exception_data      
                raise exception
    
    def get_results(self, **options):
        '''
        Returns the collected results of the executed tasks.
        
        @keyword check_fail: checks that all task are faultlessly finished. 
        
        @rtype: [object]
        '''

        check_fail = options.get('check_fail')
        if check_fail is None:
            check_fail = True
            
        if check_fail:
            self.check_fail(exception_class=options.get('exception_class'))
        else:
            self.join()
            
        return self._results
    
    def get_exceptions(self):
        '''
        Returns the collected errors of the executed tasks.
        
        @rtype: [Exception]
        '''
        
        return self._exceptions