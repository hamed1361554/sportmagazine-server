'''
Created on Feb 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from decimal import Decimal
import threading
import sys
import multiprocessing

from deltapy.core import DeltaException
from deltapy.multiprocessing.base import BasePool

def thread_worker(semaphore, queue, job_id, func, args, kwargs):
    result = None
    try:
        result = func(*args, **kwargs)
    except Exception, error:
        result = error

    try:
        queue.put((job_id, result))
    except Exception, error:
        queue.put((job_id, error))
        
    semaphore.release()

def process_worker(in_queue, out_queue, **options):
    initializer = options.get('init_func', None)
    max_threads = options.get('max_threads', 4)
    semaphore = threading.BoundedSemaphore(max_threads)
    
    if initializer:
        initializer()
    
    while True:
        job_id, func, args, kwargs = in_queue.get()
        if job_id is None:
            break
        semaphore.acquire()
        thread = threading.Thread(target=thread_worker, 
                                  args=(semaphore,
                                        out_queue, 
                                        job_id, 
                                        func, 
                                        args, 
                                        kwargs))
        thread.start()
    sys.exit(0)


class ComplexProcessWorker(threading.Thread):        
    '''
    Complex process creates a worker.
    '''
    
    def __init__(self, max_threads = 4, init_func = None):
        threading.Thread.__init__(self)
        self._in_queue = multiprocessing.Queue()
        self._out_queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(target = process_worker, 
                                                args = (self._in_queue, 
                                                        self._out_queue), 
                                                kwargs = {'max_threads' : max_threads, 
                                                          'init_func' : init_func})
        self._id = hash(self._process)        
        self._process.start()
        self._hit_count = 0
        self._requests = {}
        self._job_id = Decimal(0)
        self._keep_running = True
        
    def get_id(self):
        '''
        Returns worker ID.
        '''
        return self._id
    
    def get_hit_count(self):
        '''
        Returns hit count.
        
        @return: int
        '''
        return self._hit_count

    def _get_job_id_(self):
        self._job_id += 1
        return self._job_id
    
    def execute(self, func, *args, **kwargs):
        '''
        Executes a function in this process boundary.
        
        @param func: function
        @param *args: arguments
        @param **kwargs: keyword arguments
        @return: object 
        '''
        try:
            self._hit_count += 1
            job_id = self._get_job_id_()
            event = threading.Event()
            self._requests[job_id] = event, None
            event.clear()
            self._in_queue.put((job_id, func, args, kwargs))        
            event.wait()
            event, result = self._requests.pop(job_id)
            if isinstance(result, Exception):
                raise result
            return result
        except Exception, error:
            raise Exception(str(error))
        
    def run(self):
        '''
        Overrides run method of Thread class.
        '''
        
        while self._keep_running and self._process.is_alive():
            try:
                job_id, result = self._out_queue.get()
                event = self._requests[job_id][0]
                self._requests[job_id] = event, result
                event.set()
            except:
                pass
        
    def terminate(self):
        '''
        Terminates the worker.
        '''
        self._in_queue.put((None, None, None, None))
        self._process.join(0.010)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join()
        self._keep_running = False
        
    def join(self):
        return self._process.join()

class ProcessPoolException(DeltaException):
    pass

class ComplexProcessPool(BasePool):
    '''
    Complex process pool class
    '''    
    
    def __init__(self, max_processes, max_threads = 4, init_func = None):
        self._processes = []
        self._is_terminating = False
        self._process_index = 0
        self._max_threads = max_threads
        self._init_func = init_func
        BasePool.__init__(self, 'ComplexProcessPool', max_processes)
    
    def get_max_threads(self):
        '''
        Returns maximum thread count.
        '''
        return self._max_threads
    
    def _get_process_(self):
        self._process_index += 1
        if self._process_index >= len(self._processes):
            self._process_index = 0
        return self._processes[self._process_index]    
        
    def execute(self, func, *args, **kwargs):
        '''
        Executes given function with passed arguments.
        
        @param func: function
        @param args: function arguments
        @param kwargs: function keyword arguments        
        '''
        if self._is_terminating:
            raise ProcessPoolException('Termination is in progress.')
        
        process = self._get_process_()
        
        return  process.execute(func, *args, **kwargs)

    def get_size(self):
        '''
        Gets pool size.

        @rtype: int
        @return: pool size
        '''

        return len(self._processes)

    def _change_size_(self, old_size, size):
        '''
        It will be called when pool size is changed.
        @param old_size: previous pool size
        @param size: new pool size
        '''
        
        if size > old_size:
            for i in xrange(size - old_size):
                process =\
                    ComplexProcessWorker(max_threads = self._max_threads, 
                                         init_func = self._init_func)
                
                self._processes.append(process)
                process.start()
        else:
            for i in xrange(old_size - size):
                self._processes.pop(0)
                
    def terminate(self):
        '''
        Terminates all workers in pool.
        '''
        try:
            self._is_terminating = True

            for process in self._processes:
                process.terminate()
        finally:
            self._is_terminating = False 

    def join(self):
        '''
        Joins to all workers in pool.
        '''
        for process in self._processes:
            process.join()
                    