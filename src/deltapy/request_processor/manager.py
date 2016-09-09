'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from threading import Event

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.security.session.services import get_current_session
import deltapy.config.services as config_services
import deltapy.config.services as config
import deltapy.logging.services as logging

class RequestProcessorManagerException(DeltaException):
    pass

class TimeoutException(RequestProcessorManagerException):
    pass

class RequestProcessorManager(DeltaObject):
    '''
    Request processor manager.
    '''
    
    logger = logging.get_logger(name='requestprocessor')
    
    def __init__(self):
        DeltaObject.__init__(self)
        self._processors = {}
        self._hooks = []
        self._default_processor_name = None
        self._event = Event()
        self._event.clear()
        
    def register_request_processor_hook(self, hook):
        '''
        Registers the given hook for request processor manager.
        
        @param RequestProcessorManagerHook hook: hook instance
        '''
        
        index = 0
        for older_hook in self._hooks:
            if older_hook.get_name() == hook.get_name():
                self._hooks[index] = hook
                return
            index += 1

        self._hooks.append(hook)
        
    def get_request_processor_hooks(self):
        '''
        Returns all of the registered hooks.
        
        @rtype: list(RequestProcessorManagerHook)
        @return: request processor list
        '''
        
        return self._hooks

    def register_processor(self, processor):
        '''
        Registers given processor.
        @param processor:
        '''
        if self._default_processor_name is None:
            self.set_default_processor(processor.get_name())
        self._processors[processor.get_name()] = processor
        
    def set_default_processor(self, processor_name):
        '''
        Sets given processor as default processor.
        @param processor_name:
        '''
        self._default_processor_name = processor_name
    
    def get_processors(self):
        '''
        Returns all registered processors.
        '''
        return self._processors
    
    def get_processor(self, name = None):
        '''
        Returns registered processor using given name.
        '''
        key = self._default_processor_name
        if name is not None:
            key = name        
        if key in self._processors:
            return self._processors[key]
        raise RequestProcessorManagerException("Could'nt find processor[{name}] in registered processors.".format(name = key)) 
    
    def wait_for_ready(self):
        '''
        Waits for request processor until it's status be ready.
        '''
        
        self._event.wait()
        
    def start(self, **options):
        '''
        Starts request processor.

        @keyword processor_name: Processor to start. If it not provided,
           default processor in configs will be used.

        @note: Other options will directly pass to the processor.
        '''

        # Getting configuration store
        config_store = config.get_app_config_store('request_processor')
        default_processor_name = config_store.get('global', 'default', None)

        processor_name = options.get('processor_name')
        if processor_name is not None:
            self.set_default_processor(processor_name)
            options.pop('processor_name')

        elif default_processor_name is not None:
            self.set_default_processor(default_processor_name)            

        params = config_store.get_section_data(self._default_processor_name)
        params.update(**options)

        processor = self.get_processor()
        processor.configure(params) 
        self._event.set()

        RequestProcessorManager.logger.info('Request processor started.')

    def terminate(self, name = None):
        '''
        Terminates given processor.
        @param name:
        '''

        RequestProcessorManager.logger.info('Terminating request processor [{name}]...'.format(name = name))
        processor = self.get_processor(name)
        processor.terminate()
        RequestProcessorManager.logger.info('Request processor [{name}] terminated.'.format(name = name))
    
    def process(self, 
                request,
                **options):
        '''
        Processes the request.
        
        @param request: client request
        
        @return: Response
        '''    

        return self.get_processor().process(request, **options)

    def login(self, login_request):
        """
        Authenticates the given credentials and returns login information.

        @param instance login_request: Raw request recevied from client.

        @return: login data
        @rtype: instance
        """

        return self.get_processor().login(login_request)
    
    def logout(self, logout_request):
        '''
        Logout the user from application.
        
        @param instance logout_request: Raw request received from client.
        '''
        
        return self.get_processor().logout(logout_request)
    
    def get_info(self):
        '''
        Returns information about active request processor.
        
        @return: DynamicObject
        '''
        
        processor = self.get_processor()
        info = DynamicObject(mode = processor.get_name())
        info.update(processor.get_params())
        return info

    def set_timeout(self, timeout):
        '''
        Sets global timeout of request processor.
        
        @param timeout: timeout
        '''
        
        session = get_current_session()
        context = session.get_context()
        context['timeout'] = timeout
        session.update()
        
    def get_timeout(self):
        '''
        Returns get global timeout value.
        
        @rtype: int
        @return: timeout value
        '''
        
        session = get_current_session()
        timeout = session.get_context().get('timeout')

        if timeout is None:
            config_store = \
                config_services.get_app_config_store('request_processor')
            timeout = config_store.get('global', 'timeout')
            if timeout is not None:
                timeout = int(timeout)
        
        return timeout
    
    