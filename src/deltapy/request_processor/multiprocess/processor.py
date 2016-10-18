'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.base_processor import RequestProcessorBase, handle_request, login, logout
from deltapy.multiprocessing.process_pool import ProcessPool
import deltapy.database.services as database

class MultiProcessRequestProcessor(RequestProcessorBase):
    '''
    This processor will process every request in current process.     
    '''     
    
    def __init__(self):
        RequestProcessorBase.__init__(self, 'multiprocess')
        self._pool = None

    def configure(self, params):
        '''
        Configures request processor.
        @param params:
        '''
        
        self._params = params
        max_processes = int(params.get('max_processes', 4))
        
        self._pool =\
            ProcessPool(max_processes,
                        init_func=self.__initialize_child)

    def process(self, 
                request,
                **options):
        '''
        Processes the request.
        
        @param request: client request
        
        @return: Response
        '''

        return self._pool.execute(handle_request, 
                                  request,
                                  **options)

    def login(self, login_request):
        """
        Authenticates the given credentials and returns login information.

        @param instance login_request: Raw request recevied from client.
    
        @return: login data
        @rtype: instance
        """

        return self._pool.execute(login,
                                  login_request)

    def logout(self, logout_request):
        '''
        Logout the user from application.
        
        @param instance logout_request: Raw request received from client.
        '''
        return self._pool.execute(logout,
                                  logout_request)

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

    def __initialize_child(self):
        '''
        Initializing child process
        '''
        database.reset_pools()
        self._pool = None