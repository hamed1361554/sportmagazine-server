'''
Created on Oct 8, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import time
import os

from ConfigParser import ConfigParser, NoSectionError

from deltapy.core import DeltaObject, DynamicObject
from deltapy.core import DeltaException

class ConfigStore(DeltaObject):
    '''
    Provides general functionality on a configuration store.
    A configuration store may be a database, a file system and etc.
    '''
    
    def __init__(self, name, defaults = {}):
        DeltaObject.__init__(self)
        self._set_name_(name)
        self._defaults = defaults

    def save(self):
        '''
        Saves changes on the configuration store.
        '''
        
        raise NotImplementedError()

    def reload(self):
        '''
        Reloads and synchronizes the content of this class 
        with physical configuration store.
        '''
        
        raise NotImplementedError()

    def get(self, section, key, default_value = None):
        '''
        Returns the key value of the given section.
        If the key does not exists, It returns default value.
        
        @param section: section name
        @param key: key name
        @param default_value: default value
        @return: object
        '''
        
        raise NotImplementedError()

    def set(self, section, key, value):
        '''
        Sets the key value of the given section.
        
        @param section: section name
        @param key: key name
        @param value: value
        '''
        
        raise NotImplementedError()

    def get_sections(self):
        '''
        Returns all sections.
        
        @return: list<str>
        '''
        
        raise NotImplementedError()
    
    def get_section_data(self, section):
        '''
        Returns all section keys and values in a dictionary.
        
        @param section: section name
        @return: dict
        '''
        
        raise NotImplementedError()

    def get_keys(self, section):
        '''
        Returns all section keys in a dictionary.
        
        @param section: section name
        '''
        
        raise NotImplementedError()

    def has_section(self, section):
        '''
        Returns True, If the section is exists. 
        
        @param section: section name
        @return: True or False
        '''
        
        raise NotImplementedError()

    def has_key(self, section, key):
        '''
        Returns True, If the section and the key is exists. 
        
        @param section: section name
        @param key: key name
        @return: True or False
        '''
        
        raise NotImplementedError()
    
class StandardConfigStore(ConfigStore):
    '''
    Provides unix/linux standard configuration files.
    It uses Python standard ConfigParser library.
    '''

    #This string will replace with the directory this setting is on.
    SETTING_DIRECTORY_VARIABLE_NAME = '$SETTING_DIRECTORY'
    
    def __init__(self, name, filename, defaults):

        # Calling super class
        ConfigStore.__init__(self, name, defaults)

        # Setting file name
        self.__filename = filename

        self.__parser = None
        #Loading config for the first time.
        self.reload()

    def _create_defaults_key_(self, section, key):
        '''
        Creates a key for defaults values using section and key.
        @param section: section name
        @param key: key name
        '''
        
        head, sep, _name = self.get_name().partition('.')
        
        return '{name}.{section}.{key}'.format(name = _name,
                                               section = section,
                                               key = key)
    
    def _get_pure_config_name_(self):
        '''
        Creates a key for defaults values using section and key.
        @param section: section name
        @param key: key name
        '''
        
        head, sep, _name = self.get_name().partition('.')
        return _name
        
    def get_file_name(self):
        '''
        Returns configuration file name.
        
        @return: str
        '''
        
        return self.__filename
        
    def get(self, section, key, default_value = None):
        '''
        Returns the key value of the given section.
        If the key does not exists, It returns default value.
        
        @param section: section name
        @param key: key name
        @param default_value: default value
        @return: object
        '''
        default_key = self._create_defaults_key_(section, key)
        if default_key in self._defaults:
            result = self._defaults[default_key]            
        elif self.has_section(section) and self.has_key(section, key):
            result = self._get_parser().get(section, key)
        else:
            result = default_value

        if result is not None:        
            result = result.replace(StandardConfigStore.SETTING_DIRECTORY_VARIABLE_NAME,
                                    os.path.dirname(self.get_file_name()))
        return result

    def set(self, section, key, value):
        '''
        Sets the key value of the given section.
        
        @param section: section name
        @param key: key name
        @param value: value
        '''
        default_key = self._create_defaults_key_(section, key)
        if default_key in self._defaults:
            self._defaults[default_key] = value            

        self._get_parser().set(section, key, value)

    def save(self):
        '''
        Saves changes on the configuration store.
        '''
        pass

    def get_sections(self):
        '''
        Returns all sections.
        
        @return: list<str>
        '''
        
        sections = []
        for key in self._defaults.keys():
            if key.startswith(self._get_pure_config_name_()):
                partitions = key.split('.')
                section_index = len(partitions) -2
                if section_index > 0:                    
                    sections.append(partitions[section_index])
                                         
        return  set(self._get_parser().sections()).union(set(sections))

    def get_section_data(self, section):
        '''
        Returns all section keys and values in a dictionary.
        
        @param section: section name
        @return: dict
        '''

        data = {}
        keys = self.get_keys(section)
        for key in keys:
            value = self.get(section, key)
            data[key] = value
            
        if len(data) == 0 and not self.has_section(section):
            raise NoSectionError(section)

        return DynamicObject(data)

    def get_keys(self, section):
        '''
        Returns all section keys in a dictionary.
        
        @param section: section name
        '''
        
        head, sep, name = self.get_name().partition('.')
        keys = []
        for key in self._defaults.keys():
            if key.startswith(name):
                head, sep, tail = key.rpartition('.')
                keys.append(tail)
        options = []
        parser = self._get_parser()
        if parser.has_section(section):
            options = parser.options(section) 
        return list(set(options).union(set(keys)))

    def has_section(self, section):
        '''
        Returns True, If the section is exists. 
        
        @param section: section name
        @return: True or False
        '''
        sections = self.get_sections()
        return section in sections

    def has_key(self, section, key):
        '''
        Returns True if sections has the key.
        
        @param section: section name
        @param key: key name
        @return: True or False
        '''
        default_key = self._create_defaults_key_(section, key)
        if default_key in self._defaults:
            return True

        return self._get_parser().has_option(section, key)

    def reload(self):
        '''
        Reloads configuration.
        '''
        # Creating an instance of ConfigParser class
        parser = ConfigParser()
        #Make config parser case sensitive.
        parser.optionxform = str

        # Parsing the configuration file
        if len(parser.read(self.get_file_name())) == 0:
            
            # Raising an error, If configuration file is invalid 
            raise DeltaException('Configuration file[%s] not found.' % self.get_file_name())

        self.__parser = parser

    def _get_parser(self):
        '''
        Gets the config parser.
        It checks if configs needs to be reloaded.
        '''
        return self.__parser
