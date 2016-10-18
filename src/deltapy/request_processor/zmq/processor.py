'''
Created on Oct 15, 2014

@author: Abi.Mohammadi
'''

from Queue import Queue
from threading import Thread as Greenlet
import os
import cPickle
import threading
import multiprocessing

#from gevent.greenlet import Greenlet
import zmq
import gevent

from deltapy.request_processor.base_processor import RequestProcessorBase, handle_request
from deltapy.multiprocessing.process_pool import ProcessPool
import deltapy.database.services as database_services
import deltapy.config.services as config_services
import deltapy.logging.services as logging_services

class ZMQRequestProcessor(RequestProcessorBase):
    '''
    This processor will process every request in current process.     
    '''
    
    LOGGER = logging_services.get_logger(name='requestprocessor')     
    
    def __init__(self):
        RequestProcessorBase.__init__(self, 'zmq')
        
        # Process pool instance
        self._pool =  None
        
        # ZMQ context
        self._context = None
        
        # Facing who sends a request
        self._frontend = None
        
        # Facing who processes a request 
        self._backend = None
        
        # The distributer client
        self._dispatcher_pool = None

    def configure(self, params):
        '''
        Configures request processor.
        @param params:
        '''
        
        # Getting ZMQ parameters
        self._params = params
        
        # Getting max processes
        max_processes = int(params.get('max_processes', 4))
        max_threads = int(params.get('max_threads', 4))
        frontend_port = int(params.get('frontend_port'))
        backend_port = int(params.get('backend_port'))
        
        # Starting ZMQ Queue
        self._context = zmq.Context(1)

        self._frontend = self._context.socket(zmq.XREP)
        self._frontend.setsockopt(zmq.LINGER, 0)
        self._frontend.bind("tcp://*:{0}".format(frontend_port))
        
        self._backend = self._context.socket(zmq.XREQ)
        self._backend.setsockopt(zmq.LINGER, 0)
        self._backend.bind("tcp://*:{0}".format(backend_port))
        
        self._dispatcher_pool = Queue(max_threads * max_processes)
        for i in xrange(max_threads * max_processes):
            client = self._context.socket(zmq.REQ)
            client.setsockopt(zmq.LINGER, 0)
            client.connect("tcp://127.0.0.1:{0}".format(frontend_port))
            self._dispatcher_pool.put(client)
            
        def start_queue():
            zmq.device(zmq.QUEUE, self._frontend, self._backend)
        
        t = Greenlet(target=start_queue)
        t.start()
        #gevent.spawn(zmq.device, zmq.QUEUE, self._frontend, self._backend)
        
        # Initializing process pool
        self._pool =\
            ProcessPool(max_processes,
                        init_func = ZMQRequestProcessor.init_func)

    def process(self, 
                 request,
                 **options):
        '''
        Processes the request.
        
        @param request: client request
        
        @return: Response
        '''
        
        client = self._dispatcher_pool.get()
        
        try:
            client.send(cPickle.dumps([request, options]))
            message = client.recv()
            obj = cPickle.loads(message)
            if isinstance(obj, Exception):
                raise obj
            return obj
        finally:
            self._dispatcher_pool.put(client)

    def resize(self, size):
        '''
        Resizes current process pool.
        @param int size: pool size
        '''
        if self._pool is not None:
            return self._pool.set_size(size)

    def terminate(self):
        '''
        Terminates current request processor.
        '''

        self._pool.terminate()
        self._frontend.close()
        self._backend.close()
        self._context.term()

    @staticmethod
    def init_func():
        settings = config_services.get_app_config_store('request_processor')
        backend_port = int(settings.get('zmq', 'backend_port'))
        max_threads = int(settings.get('zmq', 'max_threads'))
        if max_threads == 0:
            max_threads = 4
        io_threads = multiprocessing.cpu_count() - 1
        if io_threads < 2:
            io_threads = 2;
            
        ZMQRequestProcessor.LOGGER.info("Process [{0}] is started as a subscriber by [{1}] greenlets.".format(os.getpid(), max_threads))
        
        database_services.reset_pools()
        context = zmq.Context(io_threads)
        
        workers = [Worker(context, backend_port) for i in xrange(max_threads)]
        
        for worker in workers:
            worker.start()
            
        for worker in workers:
            worker.join()

class Worker(Greenlet):
    def __init__(self, context, backend_port):
        super(Worker, self).__init__()

        self.socket = context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 0)
        endpoint = 'tcp://127.0.0.1:{0}'.format(backend_port)
        self.socket.connect(endpoint)
        ZMQRequestProcessor.LOGGER.info("Greenlet is connected to the backend [{0}].".format(endpoint))
        self._keep_going = True
    
    def run(self):
        while self._keep_going:
            try:
                ZMQRequestProcessor.LOGGER.info("Waiting for a message...")
                message = self.socket.recv()
                ZMQRequestProcessor.LOGGER.info("A message with size [{0}] received.".format(len(message)))
                request, options = cPickle.loads(message)
                ZMQRequestProcessor.LOGGER.info("Request [{0}] is ready to process.".format(request))
                try:
                    result = handle_request(request, **options)
                except Exception as e:
                    result = e
                ZMQRequestProcessor.LOGGER.info("Request [{0}] is handled.".format(request))
                response = cPickle.dumps(result)
                self.socket.send(response)
                ZMQRequestProcessor.LOGGER.info("Sending back the response by size [{0}].".format(len(response)))
            except Exception as e:
                ZMQRequestProcessor.LOGGER.error(e)
            
