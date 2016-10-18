'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.request_processor import APP_REQUEST_PROCESSOR
from deltapy.application.services import get_component

def resize(size):
    '''
    Resizes current process pool.
    @param size:
    '''
    return get_component(APP_REQUEST_PROCESSOR).get_processor().resize(size)

def register_request_processor_hook(hook):
    '''
    Registers the given hook for request processor manager.
    
    @param RequestProcessorManagerHook hook: hook instance
    '''
    
    return get_component(APP_REQUEST_PROCESSOR).register_request_processor_hook(hook)

def get_request_processor_hooks():
    '''
    Returns all of the registered hooks.
    
    @rtype: list(RequestProcessorManagerHook)
    @return: request processor list
    '''

    return get_component(APP_REQUEST_PROCESSOR).get_request_processor_hooks()

def register_processor(processor):
    '''
    Registers given processor.
    @param processor:
    '''
    return get_component(APP_REQUEST_PROCESSOR).register_processor(processor)

def set_default_processor(processor_name):
    '''
    Sets given processor as default processor.
    @param processor_name:
    '''
    return get_component(APP_REQUEST_PROCESSOR).set_default_processor(processor_name)

def get_processors():
    '''
    Returns all registered processors.
    '''
    return get_component(APP_REQUEST_PROCESSOR).get_processors()    

def get_processor(name = None):
    '''
    Returns registered processor using given name.
    '''
    return get_component(APP_REQUEST_PROCESSOR).get_processor(name)

def start(**options):
    '''
    Starts request processor.
    @param **options: 
    '''
    return get_component(APP_REQUEST_PROCESSOR).start(**options)

def terminate(name = None):
    '''
    Starts request processor.

    @param name: processor name 
    '''
    
    return get_component(APP_REQUEST_PROCESSOR).terminate(name)

def wait_for_ready():
    '''
    Waits for request processor until it's status be ready.
    '''
    
    return get_component(APP_REQUEST_PROCESSOR).wait_for_ready()

def get_info():
    '''
    Returns information about active request processor.
    
    @return: DynamicObject
    '''
    
    return get_component(APP_REQUEST_PROCESSOR).get_info()

def process(request, **options):
    '''
    Processes the request.
    
    @param request: client request
    
    @return: Response
    '''

    return get_component(APP_REQUEST_PROCESSOR).process(request, **options)

def login(login_request):
    """
    Authenticates the given credentials and returns login information.

    @param instance login_request: Raw request recevied from client.

    @return: login data
    @rtype: instance
    """

    return get_component(APP_REQUEST_PROCESSOR).login(login_request)

def logout(logout_request):
    '''
    Logout the user from application.
    
    @param instance logout_request: Raw request received from client.
    '''

    return get_component(APP_REQUEST_PROCESSOR).logout(logout_request)

def set_timeout(timeout):
    '''
    Sets global timeout of request processor.
    
    @param timeout: timeout
    '''
    
    return get_component(APP_REQUEST_PROCESSOR).set_timeout(timeout)
    
def get_timeout():
    '''
    Returns get global timeout value.
    
    @rtype: int
    @return: timeout value
    '''

    return get_component(APP_REQUEST_PROCESSOR).get_timeout()

def reload():
    '''
    Re-reads configs from the config file and applying them.
    '''
    return get_component(APP_REQUEST_PROCESSOR).reload()