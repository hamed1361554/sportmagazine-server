'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.request_processor.base_processor import RequestProcessorBase, handle_request, login, logout


class MultiThreadedRequestProcessor(RequestProcessorBase):
    '''
    This processor will process every request in current process.     
    '''     
    
    def __init__(self):
        RequestProcessorBase.__init__(self, 'multithread')

        self._semaphore = None

    def configure(self, params):
        '''
        Configures request processor.
        @param params:
        '''

        self._params = params

    def process(self,
                request,
                **options):
        '''
        Processes the request.

        @param request: client request

        @return: Response
        '''

        return handle_request(request, **options)

    def login(self, login_request):
        """
        Authenticates the given credentials and returns login information.
    
        @param instance login_request: Raw request recevied from client.
    
        @return: login data
        @rtype: instance
        """

        return login(login_request)

    def logout(self, logout_request):
        '''
        Logout the user from application.
        
        @param instance logout_request: Raw request received from client.
        '''
        return logout(logout_request)

    def resize(self, size):
        '''
        Resizes current process pool.
        @param int size: pool size
        '''
        pass
    
    def terminate(self):
        '''
        Terminates current request processor.
        '''
        pass
