'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

from deltapy.locals import *

def add_config_store(config_store):
    '''
    Adds the given config_store to it's cache.
    
    @param config_store:
    '''
    
    return get_app_context()[APP_CONFIG].add_config_store(config_store)

def add_std_config(name, filename):
    '''
    Creates a standard config store and adds the config_store to it's cache. 
    
    @param name:
    @param filename:
    '''
    
    return get_app_context()[APP_CONFIG].add_std_config(name, filename)

def get_config_store(name):
    '''
    Returns the config store by name.
    
    @param name: name of the config store.
    @return: ConfigStore
    '''
    
    return get_app_context()[APP_CONFIG].get_config_store(name)

def get_config_stores():
    '''
    Returns all config stores in cache.
    
    @return: [ConfigStore]
    '''
    
    return get_app_context()[APP_CONFIG].get_config_stores()

def remove_config_store(name):
    '''
    Removes the configuration store by it's name.
    
    @param name: configuration store name
    '''
    
    return get_app_context()[APP_CONFIG].remove_config_store(name)
    
   
def load_all_configs(package, extension = '.config'):
    '''
    Loads all configuration of a package by looking in settings directory.
    
    @param package: a python package
    '''

    return get_app_context()[APP_CONFIG].load_all_configs(package, extension = '.config')


def get_app_config_store(name = 'app'):
    '''
    Returns application settings.
    '''

    return get_config_store("%s.%s" % (get_app().get_name(), name))


def reload_all():
    '''
    Reloads all the configuration files. e.g. reads config files again
    and update config stores with it.
    '''

    return get_app_context()[APP_CONFIG].reload_all()
