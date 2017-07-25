"""
Created on Feb 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
"""

import os
import sys
import time
import errno
import threading
import traceback
import multiprocessing
from datetime import datetime
from random import randint

from deltapy.core import DeltaException
from deltapy.multiprocessing.base import BasePool
from deltapy.logging.services import get_logger


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


def thread_worker(semaphore, queue, job_id, func, args, kwargs):
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
        queue.put((job_id, result))
    except Exception as error:
        LOGGER.error("Error while putting result in out queue: " +
                     str(error) + traceback.format_exc())
        queue.put((job_id, error))

    semaphore.release()


def process_worker(in_queue, out_queue, threads, semaphore, **options):
    initializer = options.get('init_func', None)

    if initializer:
        initializer()

    while True:
        try:

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
            threads[job_id] = (thread, semaphore, datetime.now())
            thread.start()

        except IOError as e:
            if e.errno == errno.EINTR:
                continue
            raise
        except KeyboardInterrupt:
            print '>> Terminating worker process', os.getpid()
            break

    while len(threads) > 0:
        time.sleep(1)

    sys.exit(0)


class ComplexProcessWorker(threading.Thread):
    """
    Complex process creates a worker.
    """

    def __init__(self, max_threads=4, init_func=None):
        """
        Initializes complex process worker.

        @param max_threads: max threads
        @param init_func: initialization function
        """

        threading.Thread.__init__(self)
        self._in_queue = multiprocessing.Queue()
        self._out_queue = multiprocessing.Queue()
        self._process_threads = {}
        self._semaphore = threading.BoundedSemaphore(max_threads)
        self._process = multiprocessing.Process(target=process_worker,
                                                args=(self._in_queue,
                                                      self._out_queue,
                                                      self._process_threads,
                                                      self._semaphore),
                                                kwargs={'init_func': init_func})
        self._id = hash(self._process)
        self._process.start()
        self._hit_count = 0
        self._requests = {}
        self._job_id = 0
        self._keep_running = True

    def get_id(self):
        """
        Returns worker ID.
        """

        return self._id

    def get_hit_count(self):
        """
        Returns hit count.

        @return: int
        """

        return self._hit_count

    def get_thread_count(self):
        """
        Returns thread count.

        @return: int
        """

        return len(self._process_threads)

    def _get_job_id_(self):
        self._job_id = time.mktime(datetime.now().timetuple()) * 1000 + randint(100, 999)
        return self._job_id

    def execute(self, func, *args, **kwargs):
        """
        Executes a function in this process boundary.

        @param func: function
        @param *args: arguments
        @param **kwargs: keyword arguments
        @return: object
        """

        self._hit_count += 1
        job_id = self._get_job_id_()

        try:
            event = threading.Event()
            self._requests[job_id] = event, None
            event.clear()
            self._in_queue.put((job_id, func, args, kwargs))
            event.wait()
            event, result = self._requests.pop(job_id)
            if isinstance(result, Exception):
                raise result
            return result
        except Exception as error:
            raise Exception(str(error))
        finally:
            self._process_threads.pop(job_id)

    def run(self):
        """
        Overrides run method of Thread class.
        """

        while self._keep_running and self._process.is_alive():
            try:
                job_id, result = self._out_queue.get()
                event = self._requests[job_id][0]
                self._requests[job_id] = event, result
                event.set()
            except:
                pass

    def terminate(self):
        """
        Terminates the worker.
        """

        self._in_queue.put((None, None, None, None))
        self._process.join(0.010)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join()
        self._keep_running = False

    def join(self, timeout=None):
        """
        Wait until the thread terminates.
        """

        return self._process.join()


class ProcessPoolException(DeltaException):
    """
    Process Pool Exception
    """


class ComplexProcessPool(BasePool):
    """
    Complex process pool class
    """

    def __init__(self, max_processes, max_threads=4, init_func=None):
        """
        Initializes complex process pool.

        @param max_processes: max processes
        @param max_threads: max threads
        @param init_func: initialization function
        """

        self._processes = []
        self._is_terminating = False
        self._process_index = 0
        self._max_threads = max_threads
        self._init_func = init_func
        BasePool.__init__(self, 'ComplexProcessPool', max_processes)

    def get_max_threads(self):
        """
        Returns maximum thread count.
        """

        return self._max_threads

    def _get_process_(self):
        self._process_index += 1
        if self._process_index >= len(self._processes):
            self._process_index = 0
        return self._processes[self._process_index]

    def _get_free_process(self):
        counter = 1

        while True:
            process = self._get_process_()
            if process.get_thread_count() < self._max_threads:
                return process

            #if counter >= len(self._processes):
            #    return self._add_worker_()

            if counter > 2 * len(self._processes):
                raise DeltaException('There is no worker to serve request.')

            counter += 1

    def execute(self, func, *args, **kwargs):
        """
        Executes given function with passed arguments.

        @param func: function
        @param args: function arguments
        @param kwargs: function keyword arguments
        """

        if self._is_terminating:
            raise ProcessPoolException('Termination is in progress.')

        process = self._get_free_process()

        return process.execute(func, *args, **kwargs)

    def get_size(self):
        """
        Gets pool size.

        @rtype: int
        @return: pool size
        """

        return len(self._processes)

    def _add_worker_(self):
        """
        It will be called when there is no worker to serve.

        @param old_size: previous pool size
        @param size: new pool size
        """

        process = \
            ComplexProcessWorker(max_threads=self._max_threads,
                                 init_func=self._init_func)

        self._processes.append(process)
        process.start()

        return process

    def _change_size_(self, old_size, size):
        """
        It will be called when pool size is changed.
        @param old_size: previous pool size
        @param size: new pool size
        """

        if size > old_size:
            for i in xrange(size - old_size):
                process = \
                    ComplexProcessWorker(max_threads=self._max_threads,
                                         init_func=self._init_func)

                self._processes.append(process)
                process.start()
        else:
            for i in xrange(old_size - size):
                process = self._processes.pop(0)
                process.terminate()

    def terminate(self):
        """
        Terminates all workers in pool.
        """

        try:
            self._is_terminating = True

            for process in self._processes:
                process.terminate()
        finally:
            self._is_terminating = False

    def join(self):
        """
        Joins to all workers in pool.
        """

        for process in self._processes:
            process.join()
