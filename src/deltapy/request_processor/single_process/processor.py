'''
Created on Feb, 2015

@author: Aidin
'''

import sys
import os
import signal
import time
import multiprocessing

from deltapy.core import DeltaException
from deltapy.request_processor.base_processor import RequestProcessorBase
from deltapy.request_processor.single_process.worker_process import worker_process_main_func


class SingleProcessRequestProcessorException(DeltaException):
    '''
    Raises if any error occured in Single Process request processor.
    '''

class SingleProcessRequestProcessor(RequestProcessorBase):
    '''
    Starts child processes that each of them have their own
    communicator.
    An outer device should route requests between them.
    '''
    
    def __init__(self):
        RequestProcessorBase.__init__(self, 'single_process')
        self._max_processes =  None
        self._max_threads = None
        self._workers = []

    def configure(self, params):
        '''
        Configures request processor.
        @param params:
        '''
        
        self._params = params
        self._max_processes = int(params.get('max_processes', 16))
        self._max_threads = int(params.get('max_threads', 5))

        # Creating child processes.
        for i in xrange(self._max_processes):
            # We start numbering our workers from one, instead of zero.
            worker_number = i + 1
            worker = multiprocessing.Process(target=worker_process_main_func,
                                             args=(worker_number, self._max_threads),
                                             name="worker-{0:02}".format(i))
            worker.start()
            self._workers.append(worker)

    def process(self, 
                request,
                **options):
        '''
        Processes a request.
        '''

        raise SingleProcessRequestProcessorException("A request recieved in Single Process request processor! It's probably a bug.")

    def login(self, login_request):
        """
        Authenticates the given credentials and returns login information.
    
        @param instance login_request: Raw request recevied from client.
    
        @return: login data
        @rtype: instance
        """

        raise SingleProcessRequestProcessorException("A login request recieved in Single Process request processor! It's probably a bug.")

    def logout(self, logout_request):
        '''
        Logout the user from application.
        
        @param instance logout_request: Raw request received from client.
        '''
        raise SingleProcessRequestProcessorException("A logout request recieved in Single Process request processor! It's probably a bug.")

    def resize(self, size):
        '''
        Resizes current process pool.

        @param size: new size.
        '''
        # Nothing to do.
        pass
    
    def terminate(self):
        '''
        Terminates current request processor.
        '''
        # Telling children to terminate.
        for process in self._workers:
            process.terminate()

        # Waiting a few seconds.
        time.sleep(5)

        # Force close them if they're still alive.
        for process in self._workers:
            if process.is_alive():
                try:
                    os.kill(process.pid, signal.SIGKILL)
                except Exception:
                    print "Couldn't terminate one of child processes."
                    # Ignore it.

        sys.exit(0)
