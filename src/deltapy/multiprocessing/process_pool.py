'''
Created on Feb 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
import sys
import time
import Queue
import multiprocessing
import errno
import os
import traceback

from deltapy.core import DeltaException
from deltapy.multiprocessing.base import BasePool
from deltapy.logging.services import get_logger


LOGGER = get_logger(name='requestprocessor')


class DeltaError(DeltaException):
    
    def __init__(self, message, code=None, data={}):
        DeltaException.__init__(self, message)
        self._code = self.__class__.__name__
        if code is not None:
            self._code = code
        self._data = data

    def get_code(self):
        return self._code


def process_worker(in_queue, out_queue, **options):

    initializer = options.get('init_func', None)   
    if initializer:
        initializer()
    
    while True:
        try:
            func, args, kwargs = in_queue.get()
            if func is None:
                break
            result = None
            
            try:
                result = func(*args, **kwargs)
            except DeltaException as delta_error:
                LOGGER.error("Error while executing func [{0}]: ".format(func.__name__) +\
                             str(delta_error) + traceback.format_exc())
                result = DeltaError(str(delta_error), code=delta_error.get_code(), data=delta_error.get_data())
            except Exception as error:
                LOGGER.error("Error while executing func [{0}]: ".format(func.__name__) +\
                             str(error) + traceback.format_exc())
                result = error
    
            try:
                out_queue.put(result)
            except Exception as error:
                LOGGER.error("Error while putting result in out queue: " +\
                             str(error) + traceback.format_exc())
                out_queue.put(error)
        except IOError as e:
            if e.errno == errno.EINTR:
                continue
            raise
        except KeyboardInterrupt:
            print '>> Terminating worker process', os.getpid()
            break

    sys.exit(0)

class ProcessPoolException(DeltaException):
    pass

class ProcessPool(BasePool):
    '''
    Process pool class
    '''
    
    def __init__(self, size, init_func = None):
        self._processes = Queue.Queue()
        self._busy_processes = {}
        self._is_terminating = False
        self._init_func = init_func
        BasePool.__init__(self, 'ProcessPool', size)
        
        
    def execute(self, func, *args, **kwargs):
        '''
        Executes given function with passed arguments.
        
        @param func: function
        @param args: function arguments
        @param kwargs: function keyword arguments        
        '''
        if self._is_terminating:
            raise ProcessPoolException('Termination is in progress.')

        process, in_q, out_q = self._processes.get()

        try:
            self._busy_processes[process] = process
            in_q.put((func, args, kwargs))
            result = out_q.get()
            if isinstance(result, Exception):
                raise result        
            return result

        finally:
            if not self._is_terminating:
                # Return back the process to the pull.
                self._busy_processes.pop(process)
                self._processes.put((process, in_q, out_q))
            else:
                # Don't return the process to pull. Instead, try to terminate it
                self._terminate_process(process, in_q, out_q)

    def _change_size_(self, old_size, size):
        '''
        It will be called when pool size is changed.
        @param old_size: previous pool size
        @param size: new pool size
        '''
        
        if size > old_size:
            for i in xrange(size - old_size):
                in_queue = multiprocessing.Queue()
                out_queue = multiprocessing.Queue()
                process =\
                    multiprocessing.Process(target = process_worker,
                                            args = (in_queue, out_queue),
                                            kwargs = {'init_func' : self._init_func})
                self._processes.put((process, in_queue, out_queue))
                
                process.start()
        else:
            for i in xrange(old_size - size):
                process, in_q, out_q, = self._processes.get()
                self._terminate_process(process, in_q, out_q)

    def terminate(self):
        '''
        Terminates all workers in pool.
        '''
        self._is_terminating = True
        while self._processes.qsize() > 0:
            try:
                process, in_q, out_q, = self._processes.get(block=False)
            except Exception:
                # There maybe an exception in the queue became empty right after
                # condition of `while' checked. We simply ignore it.
                continue
            # If there wasn't any error getting the process, terminate it.
            self._terminate_process(process, in_q, out_q)

        if len(self._busy_processes) > 0:
            # Wait 5 seconds for these processes to terminate.
            time.sleep(5)
        
        while len(self._busy_processes) > 0:
            # There's still some processes in queue. Kill them by force!
            try:
                # Popping first process from the busy dictionary.
                process = self._busy_processes.pop(self._busy_processes.keys()[0])
            except Exception:
                # There maybe an exception in the queue became empty right after
                # condition of `while' checked. We simply ignore it.
                continue

            try:
                os.kill(process.pid, 9)
            except Exception as error:
                print "Couldn't kill the child process, because of error:", str(error)

    def join(self):
        '''
        Joins to all workers in pool.
        '''
        for process in self._busy_processes.values():
            process.join()
           
        while self._processes.qsize() > 0:
            process, in_q, out_q, = self._processes.get()
            process.join()
    
    def _terminate_process(self, process, in_q, out_q):
        '''
        Terminates the specified workder process.
        '''
        try:
            in_q.put((None, None, None))
            process.join(0.010)
            if process.is_alive():
                process.terminate()
                process.join(0.050)

                if process.is_alive():
                    print "Process {0}, didn't stop after 50ms, trying to kill it...".format(process.pid)
                    try:
                        os.kill(process.pid, 9)
                    except Exception as error:
                        print "Couldn't kill the child process, because of error:", str(error)

        except Exception:
            print "Could not stop process {0}, trying to kill it...".format(process.pid)
            try:
                os.kill(process.pid, 9)
            except Exception as error:
                print "Couldn't kill the child process, because of error:", str(error)
