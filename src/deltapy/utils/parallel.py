'''
Created on Sep 1, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
from timecounter import TimeCounter
import threading
import Queue
import time

class DynamicSemaphore:
    """
    dynamic semaphore class.
    """
    def __init__(self, max_size):
        """
        class initialization.
        """
        self._max =  max_size
        self._count = 0
        self._event = threading.Event()
        self._event.set()
        self._lock = threading.Lock()
        self._set_lock = threading.Lock()
        
    def acquire(self):
        """
        acquire lock.
        """
        self._lock.acquire()
        
        if self._count >= self._max - 1:
            self._event.clear()

        self._event.wait()
        self._increment()
        
        self._lock.release()
        
    def release(self):
        """
        release lock.
        """
        self._decrement()
        if self._count < self._max - 1:
            self._event.set()
        
    def _increment(self):
        """
        increment size.
        """
        self._set_lock.acquire()
        self._count += 1
        self._set_lock.release()

    def _decrement(self):
        """
        decrement size.
        """
        self._set_lock.acquire()
        self._count -= 1
        self._set_lock.release()
    
    def resize(self, new_max):
        """
        change max size.
        """
        self._set_lock.acquire()
        self._max = new_max
        self._set_lock.release()

class ParallelTask(threading.Thread):
    """
    Parallel Task class.
    """
    def __init__(self, parallel_executer, execute_func, params):
        """
        parallel task initialization.
        """
        threading.Thread.__init__(self)
        self._parallel_executer = parallel_executer
        self._execute_func = execute_func
        self._params = params
        
    def run(self):
        """
        run method of class.
        """
        try:
            self._execute_func(self._params)
        except Exception, e:
            print str(e)
        self._parallel_executer.release()
    
class ParallelExecutor(threading.Thread):
    """
    parallel executor class.
    this class executes parallel task using central parameter queue.it manages thread pool and 
    parallel task count.
    """
    def __init__(self, execute_func, thread_count = 1, before_run_task = None, after_run_task = None):
        threading.Thread.__init__(self)
        self._queue = Queue.Queue()
        self._execute_func = execute_func
        self._threads = []
        self._is_running = False
        self._before_run = before_run_task
        self._after_run = after_run_task
        self._event = threading.Event()
        self._event.set()
        self._thread_count = thread_count
        self._before_run_task_time = 0
        self._after_run_task_time = 0
        self._pure_run_time = 0
        self._time_counter = TimeCounter()
        self._semaphore = None
        self._startTime = None
        
    def add_parameter(self, parameter):
        """
        adding new parameter to centeral parameter queue
        """
        self._queue.put(parameter)

    def add_parameters(self, parameters):
        """
        adding a list of parameters to centeral parameter queue
        """
        for param in parameters:
            self._queue.put(param)
        
    def run(self):
        """
        runs parallel executer.
        """
        try:
            if self._is_running :
                raise Exception('The parallel executer is running.')

            self._time_counter.start_counter("beforeRunTask")
            if self._before_run is not None:
                self._before_run(self)
            self._before_run_task_time = \
                self._time_counter.get_counter("beforeRunTask")

            self._time_counter.start_counter("pureRunTask")
            self._is_running  = True
            self._startTime = time.time()
            self._semaphore = DynamicSemaphore(self._thread_count + 1)
            self._threads = []
            while not self._queue.empty() and self._is_running:
                self._event.wait()
                self._acquire()
                params = self._queue.get()
                task = ParallelTask(self, self._execute_func, params)
                self._threads.append(task)
                task.start()

            for thread in self._threads:
                thread.join()

            self._pure_run_time = self._time_counter.get_counter("pureRunTask")

            self._time_counter.start_counter("afterRunTask")
            if self._after_run is not None:
                self._after_run(self)
            self._after_run_task_time = \
                self._time_counter.get_counter("afterRunTask")
        finally:
            self._is_running = False
        
    def wait_for_complete(self):
        """
        this function waits for completing all running tasks.
        """
        self.join()
        return time.time() - self._startTime

    def reset(self):
        """
        this function resets parallel executer and also resets parameter queue.
        """
        self.stop()
        self._queue = Queue.Queue()
    
    def stop(self):
        """
        stops parallel executer.
        """
        self._is_running = False
        
    def pause(self):
        """
        pause all tasks of parallel executer.
        """
        self._event.clear()
        
    def work(self):
        """
        work method.
        """
        self._event.set()
        
    def resize(self, thread_count):
        """
        resize parallel thread count.
        """
        self._thread_count = thread_count
        self._semaphore.resize(thread_count + 1)
                
    def is_running(self):
        """
        returns True if parallel executer working.
        """
        return self._is_running
    
    def _acquire(self):
        """
        acquire semaphore lock.
        """
        self._semaphore.acquire()
    
    def _release(self):
        """
        release semaphore lock.
        """
        self._semaphore.release()
    
    def get_elapsed_times(self):
        """
        returns elapsed time.
        """
        return self._before_run_task_time, self._pure_run_time, self._after_run_task_time
