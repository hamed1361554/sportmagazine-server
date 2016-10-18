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
import signal
import threading

from deltapy.core import DeltaException
from deltapy.multiprocessing.base import BasePool
from deltapy.logging.services import get_logger
from deltapy.request_processor.services import reload


LOGGER = get_logger(name='requestprocessor')


class DeltaError(DeltaException):
    
    def __init__(self, message, code=None, data={}, traceback=None):
        DeltaException.__init__(self, message)
        self._code = self.__class__.__name__
        if code is not None:
            self._code = code
        self._data = data
        self._traceback = traceback

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
                LOGGER.error("Error while executing func [{0}]: ".format(func.__name__) +
                             str(delta_error) + traceback.format_exc())
                result = DeltaError(str(delta_error),
                                    code=delta_error.get_code(),
                                    data=delta_error.get_data(),
                                    traceback=traceback.format_exc())
            except Exception as error:
                LOGGER.error("Error while executing func [{0}]: ".format(func.__name__) +
                             str(error) + traceback.format_exc())
                # Putting traceback in exception, so the parent process knows
                # the real traceback of the exception.
                setattr(error, 'traceback', traceback.format_exc())
                result = error

            try:
                out_queue.put(result)
            except Exception as error:
                LOGGER.error("Error while putting result in out queue: " +
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
        self._lock = threading.Lock()
        BasePool.__init__(self, 'ProcessPool', size)

        # To collect defunct processes, child signal must be listened.
        signal.signal(signal.SIGCHLD, self._dead_collector)

    def _dead_collector(self, signal_number, stack_frame):
        if self._is_terminating:
            return

        # To overcome concurrency problems, only single operation is allowed.
        keys = self._busy_processes.keys()

        # Here, I have to check both idle and busy processes, because
        # spawning process on child thread will not register signal handler.
        # See: https://stackoverflow.com/questions/37430633/forking-a-child-in-another-thread-parent-doesnt-receive-sigchld-on-termination
        with self._lock:
            for process in keys:
                if not process.is_alive():
                    out_q = self._busy_processes.get(process)
                    if out_q is not None:
                        out_q.put(Exception(_('Processing current request encounters an error.')))

            # Why I write this code to check idle processes?
            # The processes queue is multi access, while I iterating over it,
            # it will be changed, most likely. Of course, there is no way to
            # get lock over it, it's an overkill. Another way I can think of
            # is to instantiate another queue, which is not a good idea.
            queue_size = self._processes.qsize()
            for i in xrange(queue_size):
                try:
                    process, in_q, out_q = self._processes.get_nowait()
                    if process.is_alive():
                        self._processes.put((process, in_q, out_q))
                except Queue.Empty:
                    break
                except:
                    continue

            # Forcing re-spawin of dead processes.
            reload()

    def execute(self, func, *args, **kwargs):
        '''
        Executes given function with passed arguments.
        
        @param func: function
        @param args: function arguments
        @param kwargs: function keyword arguments        
        '''

        if self._is_terminating:
            raise ProcessPoolException('Termination is in progress.')

        is_alive = False
        process = None
        in_q = None
        out_q = None

        # Avoding dead processes in the pool (They may killed by a signal or
        # something. This happened in Live Environment.
        while not is_alive:
            process, in_q, out_q = self._processes.get()
            is_alive = process.is_alive()

        is_terminated = False

        try:
            self._busy_processes[process] = out_q
            in_q.put((func, args, kwargs))
            result = out_q.get()
            if isinstance(result, Exception):
                raise result
            return result
        except MemoryError:
            if not self._is_terminating:
                self._terminate_process(process, in_q, out_q)
                is_terminated = True
                raise
        finally:
            if not self._is_terminating:
                # Return back the process to the pull.
                self._busy_processes.pop(process)
                if not is_terminated and process.is_alive():
                    self._processes.put((process, in_q, out_q))
            else:
                # Don't return the process to pull. Instead, try to terminate it
                self._terminate_process(process, in_q, out_q)

    def get_size(self):
        '''
        Gets pool size.

        @rtype: int
        @return: pool size
        '''

        return self._processes.qsize() + len(self._busy_processes)

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
                process = \
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
                process = self._busy_processes.keys()[0]
                self._busy_processes.pop(process)
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
        for process in self._busy_processes.keys():
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
