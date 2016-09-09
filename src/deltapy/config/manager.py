'''
Created on Aug 13, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import os

from deltapy.core import DeltaException
from deltapy.core import DeltaObject
from deltapy.utils import get_module_dir
from deltapy.config.config_store import StandardConfigStore

class ConfigManagerException(DeltaException):
    '''
    Configuration manager error class
    '''
    pass

class ConfigFileNotFoundException(ConfigManagerException):
    '''
    Configuration manager error class
    '''
    pass

class ConfigManager(DeltaObject):
    '''
    A class for managing configuration stores.
    '''
    
    SETTINGS_FOLDER_NAME = 'settings'

    def __init__(self,
                 default_settings_folder_name = 'settings',
                 defaults = {}):
        # Calling the super class
        DeltaObject.__init__(self)
        
        # Setting default configuration folder name.
        self.__default_settings_folder_name = default_settings_folder_name
        
        # Configuration stores
        self.__config_stores = {}
        
        # Setting default options
        self._defaults = defaults
        
    def get_config_store_by_file_name(self, file_name):
        '''
        Returns configuration store by given full file path.
        
        @param file_name: full file path
        @return: ConfigStore
        '''
        
        for config_store in self.get_config_stores():
            if config_store.get_file_name() == file_name:
                return config_store
        return None
    
    def reload_all(self):
        '''
        Reloads all the configuration files. e.g. reads config files again
        and update config stores with it.
        '''
        for config_store in self.get_config_stores():
            config_store.reload()

    def reload_config_store(self, path, added_list, removed_list, changed_list):
        '''
        Will be called when a configuration file added or removed or changed.
        
        @param path: settings path
        @param added_list: added files 
        @param removed_list: removed files
        @param changed_list: changed files
        '''
        
        if len(changed_list) > 0:
            for base_file_name in changed_list:
                file_name = os.path.join(path, base_file_name)
                config_store = self.get_config_store_by_file_name(file_name)
                if config_store:
                    config_store.reload() 

    def add_config_store(self, config_store):
        '''
        Adds the given config_store to it's cache.
        
        @param config_store:
        '''
        
        if config_store.get_name() in self.__config_stores:
            raise Exception('Configuration[%s] already exists.' % config_store.get_name())
        self.__config_stores[config_store.get_name()] = config_store
    
    def add_std_config(self, name, filename):
        '''
        Creates a standard configuration store and adds the config_store to it's cache. 
        
        @param name:
        @param filename:
        '''
        
        self.add_config_store(StandardConfigStore(name, filename, self._defaults))
    
    def get_config_store(self, name):
        '''
        Returns the configuration store by name.
        
        @param name: name of the configuration store.
        @return: ConfigStore
        '''
        
        if name not in self.__config_stores:
            raise ConfigFileNotFoundException('Configuration [%s] not found.' % name)
        return self.__config_stores[name]
    
    def get_config_stores(self):
        '''
        Returns all configuration stores in cache.
        
        @return: [ConfigStore]
        '''
        
        return self.__config_stores.values()
    
    def remove_config_store(self, name):
        '''
        Removes the configuration store by it's name.
        
        @param name: configuration store name
        '''
        if name not in self.__config_stores:
            raise DeltaException('Configuration[%s] not found.' % name)
        del self.__config_stores[name]
        
    def load_all_configs(self, package, extension = '.config'):
        '''
        Loads all configuration of a package by looking in settings directory.
        
        @param package: a python package
        '''

        package_dir = get_module_dir(package)
        settings_dir = os.path.join(package_dir, 
                                    ConfigManager.SETTINGS_FOLDER_NAME)
        
        config_files = {}
        if os.path.exists(settings_dir):
            for file_name in os.listdir(settings_dir):
                if file_name.endswith(extension):
                    config_files[file_name] = os.path.join(settings_dir, file_name)

       
        if self.__default_settings_folder_name is not None:
            if self.__default_settings_folder_name != ConfigManager.SETTINGS_FOLDER_NAME:
                new_settings_dir = os.path.join(package_dir, 
                                               self.__default_settings_folder_name)
                
                if os.path.exists(new_settings_dir):
                    settings_dir = new_settings_dir
                    for file_name in os.listdir(settings_dir):
                        if file_name.endswith(extension):
                            config_files[file_name] = os.path.join(settings_dir, file_name)

        for file_name in config_files:
            file_path = config_files[file_name]
            alias = "%s.%s" % (str(package), file_name.replace(extension, ''))
            self.add_std_config(alias, file_path)
