'''
Created on Aug 14, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''


import sys
import os
import signal

from deltapy.packaging.manager import PackageManager
from deltapy.core import DeltaObject
from deltapy.core import DeltaException
from deltapy.utils import get_module_dir
from deltapy.utils import get_package_of
from deltapy.core import Context
from deltapy.locals import APP_PACKAGING, _set_app_

import deltapy.packaging.services as packaging
import deltapy.communication.services as communication
import deltapy.event_system.services as event_system_services

class ApplicationException(DeltaException):
    '''
    Contains application errors.
    '''
    pass

class ApplicationContext(Context):
    '''
    Application context class.
    Every application saves important manager classes or 
    some important data in this class.
    '''
    pass

class Application(DeltaObject):
    '''
    It is applications base class and provides application basic functionality. 
    '''
    
    class StatusEnum:
        '''
        Application status enum.
        '''
        
        READY = 'Ready'
        LOADING = 'Loading'
        RUNNING = 'Running'
        TERMINATED = 'Terminated'
        
    def __init__(self):
        
        # Calling super class        
        DeltaObject.__init__(self)
        
        # Setting this application instance in a global variable
        _set_app_(self)
        
        self.__instance_name = None
        self.__options = {}
        self.sub_app_proxies = {}
        self.context = ApplicationContext()
        self.parent_proxy = None        
        print ">> Initializing application[%s] ..." % self.get_name()

        # Loading package manager...
        self.context[APP_PACKAGING] = PackageManager()
        
    def get_default_settings_folder_name(self):
        '''
        Returns default settings folder name.
        
        @return: str
        '''
        
        default_config_folder_name = 'settings'
        
        if self.get_instance_name() is not None:
            default_config_folder_name = \
                os.path.join('settings',
                             self.get_instance_name())
        
        return self.__options.get('config_folder_name', 
                                  default_config_folder_name)
        
    def get_context(self):
        '''
        Returns application context.
        '''
        
        return self.context
        
    def get_options(self):
        '''
        Returns applications options.
        
        @return: {}
        '''
        
        return self.__options

    def get_name(self):
        '''
        Returns application's name.
        
        @return: str
        '''
        
        path = get_module_dir(self.__class__.__module__)
        head, sep, tail = path.rstrip(os.path.sep).rpartition(os.path.sep)
        return tail
    
    def get_instance_name(self):
        '''
        Returns application's instance name.
        
        @return: str
        '''
        
        return self.__instance_name

    def get_full_name(self):
        '''
        Returns application's full name.
        
        @return: str
        '''
        name = self.get_name()
        instance_name = self.get_instance_name()
        if instance_name not in (None, ''):
            name += '.{0}'.format(instance_name)
        return name

    def load(self, *args, **kargs):        
        '''
        Loads application packages.
        '''        
        
        packaging.load('deltapy.event_system')
        
        event_system_services.register_event('application.start', self._start_requirements_)
        event_system_services.register_event('application.stop', self._stop_requirements_)

        # Loading packages
        current_package = get_package_of('deltapy')
        packaging.load(current_package)
        
        # Setting application status to ready
        self._set_status_(Application.StatusEnum.READY)

        import deltapy.application.commands

        current_package = get_package_of(self.get_name())
        packaging.load(current_package)        
        print ">> Application[%s] loaded." % self.get_name()
        
    def _start_requirements_(self):
        '''
        Starts requirement packages.
        '''

        pass

    def run(self, *args, **kargs):            
        '''
        Runs the application.
        '''
        
        # Getting application instance name
        self.__instance_name = kargs.get('instance_name', None) 

        # Getting options
        self.__options.update(kargs.get('options', self.__options))
        
        self.context['__app_options__'] = self.__options
        
        #Setting process name.
        self._set_process_title()

        self._set_status_(Application.StatusEnum.LOADING)
        print ">> Loading application[%s]." % self.get_name()
        self.load(*args, **kargs)
        
        #self._start_requirements_()
        event_system_services.fire('application.start')
        
        # Getting parent information
        parent_info = kargs.get('parent_info', None)
        
        # Connecting to parent application, If the parent application
        # is determined.
        if parent_info:
            # Connecting to parent application...
            parent_name = parent_info.get('name', None)
            parent_ticket = parent_info.get('ticket', None)
            if not parent_ticket:
                raise ApplicationException('Parent application ticket is not determined.')

            print ">> Connecting to parent application[%s]." % (parent_name)
            
            # Getting listener information
            parent_listener_info = kargs.get('listener_info', None)
            
            # Creating the parent proxy
            self.parent_proxy = \
                communication.create_proxy_by_ticket(parent_ticket, 
                                                     self.get_name(), 
                                                     **parent_listener_info)

            import deltapy.security.authentication.services as authentication_services
            # Creating a ticket for parent application
            ticket = authentication_services.internal_login(parent_name, force = True)

            # Getting listener parameters
            listener_params = communication.get_listener_params(communication.get_default_listener().get_name())
            
            # Enlisting this application on parent application.
            self.parent_proxy.execute('app.enlist',
                                      self.get_name(),
                                      self.get_instance_name(),
                                      parent_name,
                                      ticket,
                                      dict(listener_params))
        
        self._set_status_(Application.StatusEnum.RUNNING)

        signal.signal(signal.SIGTERM, self.terminate)

        # while True:
        #     try:
        #         signal.pause()
        #     except KeyboardInterrupt:
        #         print "Keyboard interrupt received."
        #         self.terminate()
        #         break
        #     except Exception, error:
        #         print error
            

    def _stop_requirements_(self):
        '''
        Starts requirement packages.
        '''
    
    def terminate(self, *args):
        '''
        Terminates the application.
        '''

        print ">> Terminating application[%s]... " % self.get_name()

        # Forcing termination after 12 seconds.
        signal.alarm(12)

        event_system_services.fire('application.stop')
        self._set_status_(Application.StatusEnum.TERMINATED)

        sys.exit(0)

    def get_status(self):
        '''
        Returns the application status.
        
        READY = 0
        LOADING = 1
        RUNNING = 2
        TERMINATED = 3
        
        Mapped in Application.StatusEnum class
        
        @return: int
        '''
        return self.__status
    
    def _set_status_(self, status):
        '''
        Sets application status.
        
        @param status: application status
        '''
        self.__status = status
    
    def enlist_app(self,
                   app_name, 
                   instance_name,
                   user_name, 
                   ticket, 
                   listener_params):
        """
        Enlists an application into current application as child.
        
        @param app_name: name of child application.
        @param instance_name: application instance name. 
        @param user_name: user of child application.
        @param ticket: communication identification ticket.
        @param listener_params: communication parameters.
        """
        
        # Creating a proxy to child application
        proxy = communication.create_proxy_by_ticket(ticket, 
                                                     user_name,
                                                     **listener_params)
        
        # Saving child proxy in sub_app_proxies 
        self.sub_app_proxies[(app_name, instance_name)] = proxy
        
        print ">> Application[%s-%s] enlisted. %s" % (app_name, instance_name, ticket)

    def delist_app(self,
                   app_name, 
                   instance_name):
        """
        Delists an application into current application as child.
        
        @param app_name: name of child application.
        @param instance_name: application instance name. 
        """
        
        # Delisting child proxy from sub_app_proxies 
        if len(self.sub_app_proxies) > 0 and (app_name, instance_name) in self.sub_app_proxies:  
            self.sub_app_proxies.pop((app_name, instance_name))
        
        print ">> Application[%s-%s] delisted." % (app_name, instance_name)

    def register_component(self, name, instance):
        '''
        Registers a component in application context.
        
        @param name: component name
        @param instance: a instance of the component
        '''
        
        self.context[name] = instance
        
    def unregister_component(self, name):
        '''
        Unregisters the component from the application context by the given name.
        
        @param name: component name 
        '''
        
        if name not in self.context:
            raise ApplicationException('Component[%s] not exists in application context.' % name)
        
        self.context.pop(name) 
        
    def get_component(self, name):
        '''
        Returns the component using the given name.
        
        @param name: component name
        @return: object
        '''
        
        if name not in self.context:
            raise ApplicationException('Component[%s] not exists in application context.' % name)
        
        return self.context[name]
    
    def introduce(self):
        '''
        Introduces the application.
        '''       
        pass

    def get_application_dir(self):
        '''
        Returns application running path.
        
        @rtype: str
        '''
        
        return get_module_dir(self.__class__.__module__)

    def _set_process_title(self):
       '''
       Sets process name to `python - {full-name}'
       if `setproctitle' module is available.
       '''
       try:
           import setproctitle
           setproctitle.setproctitle('python - {0}'.format(self.get_full_name()))
       except ImportError:
           print "Warning: Could not change process title, because `setproctitle' not found."
       except Exception as error:
           print 'Warning: Could not change process title, because of the following error:', error

