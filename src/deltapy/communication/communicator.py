'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
@summary: A module for communicator related classes and functions.
'''

import traceback

from deltapy.core import DeltaObject
from deltapy.core import DeltaException
from deltapy.utils.locals import run_in_thread
from deltapy.locals import get_app

import deltapy.config.services as config
import deltapy.request_processor.services as request_processor
import deltapy.logging.services as logging


class CommunicatorException(DeltaException):
    '''
    For handling communicator errors.  
    '''
    pass

class Communicator(DeltaObject):
    '''
    The communicator class which is for maintaining listeners.
    '''
    logger = logging.get_logger(name = 'communicator')
    
    def __init__(self):
        '''
        The constructor.
        '''
        
        DeltaObject.__init__(self)
        self.__factories = {}
        self.__listeners = {}
        self.__default_listener_name = None
        self.__hooks = []
        
    def register_factory(self, type_name, factory):
        '''
        Registers a listener.
        
        @param listener: listener object which inherited from the Listener class
        '''
        
        self.__factories[type_name] = factory
        
    def get_factory(self, type_name):
        '''
        Return broker factory by broker type name.
        
        @param type_name: type name
        @return: CommunicationFactory
        '''
        if type_name not in self.__factories:
            raise CommunicatorException('Factory[%s] not found.' % type_name)
        return self.__factories[type_name]
        
    def get_listener(self, name):
        '''
        Returns the listener by name.
        
        @param name: name of the listener in str
        @return: listener[Listener]
        '''
                        
        # Looking for listener...
        if name not in self.__listeners:
            raise CommunicatorException('Listener[%s] is not registered.' % name)
        
        # Getting listener...
        listener, thread = self.__listeners[name]
        
        return listener
    
    def get_listeners(self):
        """
        Returns all listeners
        
        @return: list<Listener>
        """
        
        return [listener for listener, thread in self.__listeners.values()]
    
    def _get_listener_settings_(self, config_store=None):
        '''
        Returns listener settings.
        
        @return: dict
        '''
        listener_settings = {}
        if config_store is None:
            config_name = "%s.communication" % get_app().get_name() 
            config_store = config.get_config_store(config_name)

        sections = config_store.get_sections()
        self.__default_listener_name = config_store.get('global', 'default', None)
        for name in sections:
            if name != 'global':
                data = config_store.get_section_data(name)
                if not data.has_key('type'):
                    raise CommunicatorException('Listener[%s] has not type.' % name)
                listener_settings[name] = data
                if self.__default_listener_name is None:
                    self.__default_listener_name = name
        return listener_settings
    
    def start(self, config_store=None):
        '''
        Starts all listeners which is defined in communication configuration.
        '''
        Communicator.logger.info('Starting communicator.')
        
        try:
            listener_settings = self._get_listener_settings_(config_store)
            
            for listener_name in listener_settings:
                kwargs = listener_settings[listener_name]
                type_name = kwargs['type']
                factory = self.get_factory(type_name)
                listener = factory.create_listener(self, listener_name, kwargs)
                self.__listeners[listener_name] = listener, None
                Communicator.logger.info('Listener[{lname}] created with params[{lparam}].'.format(lname = listener_name, lparam=kwargs))

            for listener_name in self.__listeners:
                listener, thread = self.__listeners[listener_name]
                Communicator.logger.info('Starting listener[{lname}]...'.format(lname = listener_name))
                thread = run_in_thread(listener.start)
                self.__listeners[listener_name] = listener, thread
                Communicator.logger.info('Listener[{lname}] started.'.format(lname = listener_name))
                
            Communicator.logger.info('Communicator started successfully.')
        except Exception:
            Communicator.logger.error('Starting communicator failed:%s' % (traceback.format_exc()))
            raise
            

    def stop(self, force = False):
        '''
        Stops all listeners.
        
        @param force: 
        '''
        
        try:

            Communicator.logger.info('Stopping communicator started.')
            threads = []
            for listener_name in self.__listeners:
                listener, thread = self.__listeners[listener_name]
                Communicator.logger.info('Stopping listener[{lname}]...'.format(lname = listener_name))
                listener.stop(force)
                Communicator.logger.info('Listener[{lname}] stopped.'.format(lname = listener_name))
                threads.append(thread)
            
            if not force:
                for t in threads:
                    t.join()
            
            Communicator.logger.info('Stopping request processor...')                
        except Exception:
            Communicator.logger.error('Stopping communicator failed:%s' % (traceback.format_exc()))
            raise

                
    def create_proxy_by_ticket(self, ticket, user_name, **kwargs):
        '''
        Creates a proxy on the given broker type and returns it.
        
        @param ticket: security ticket
        @param user_name: user name
        @return: Proxy 
        '''
        
        type_name = kwargs.get('type')
        factory = self.get_factory(type_name)
        return factory.create_proxy_by_ticket(ticket, user_name, **kwargs)
    
    def create_proxy(self, user_name, password, **kwargs):
        '''
        Creates a proxy on the given broker type and returns it.
        
        @param user_name: user name
        @param password: password
        @return: Proxy 
        '''
        
        type_name = kwargs.get('type')
        factory = self.get_factory(type_name)
        return factory.create_proxy(user_name, password, **kwargs)

    def get_listener_params(self, name):
        '''
        Returns the listener parameters.
        
        @param name: listener name
        @return: dict 
        '''
        
        return self.get_listener(name).get_params()
    
    def get_default_listener(self):
        """
        Returns the default listener.
        
        @return: Listener
        """
        
        return self.get_listener(self.__default_listener_name)
    

    def login(self, listener, login_request):
        '''
        Logins in application.
        
        @param instance login_request: Client's login request.
        @type login_request: Instance of RawRequest.

        @return: dict<ticket,
                      login_date,
                      data>
        '''
        
        if not listener.is_enable():            
            Communicator.logger.error('Listener[%s] is disabled.' % listener.get_name())
            raise CommunicatorException('Listener[%s] is disabled.' % listener.get_name())

        try:
            return request_processor.login(login_request)

        except Exception:
            Communicator.logger.error(traceback.format_exc())
            raise

    def logout(self, listener, logout_request):
        '''
        Log outs the user.
         
        @param instance logout_request: Client's logout request.
        @type logout_request: Instance of RawRequest.
        '''

        if not listener.is_enable():
            Communicator.logger.error('Listener[%s] is disabled.' % listener.get_name())
            raise CommunicatorException('Listener[%s] is disabled.' % listener.get_name())

        return request_processor.logout(logout_request)

    def execute(self, listener, request, **options):
        '''
        Executes the given request.
        
        @param listener: listener instance
        @param request: client request
        
        @return: object
        '''    
        
        try:
            if not listener.is_enable():
                raise CommunicatorException('Listener[%s] is disabled.' % 
                                            listener.get_name())

            # Processing the request.
            return request_processor.process(request, **options)

        except Exception:
            Communicator.logger.error(traceback.format_exc())
            raise

    
    def add_hook(self, hook):
        '''
        Sets communicator hook.
        
        @param hook: hook
        '''
        
        self.__hooks.append(hook)
        
    def get_hooks(self):
        '''
        Returns communicator hook.
        
        @return: CommunicatorHook
        '''
        
        return self.__hooks
    
