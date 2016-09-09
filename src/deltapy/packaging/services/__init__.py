'''
Created on Aug 14, 2009

@author: mohammadi
'''

from deltapy.locals import *

def load(package_name):
    '''
    Loads the package and it's sub packages.
    
    @param package_name: package name
    '''
    return get_app_context()[APP_PACKAGING].load(package_name)
        
def unload(package_name):
    '''
    Unloads the package completely.
    
    @param package_name: package name
    '''
    return get_app_context()[APP_PACKAGING].unload(package_name)

def reload(package_name):
    '''
    Reloads the package.
    
    @param package_name: package name
    '''
    return get_app_context()[APP_PACKAGING].reload(package_name)
    
def get_loaded_packages(parent_name = None):
    '''
    Returns all loaded package in parent package domain.
    
    @param parent_name: parent package name
    @return: list<Package>
    '''
    return get_app_context()[APP_PACKAGING].get_loaded_packages(parent_name)

def get_disabled_packages():
    '''
    Returns all disabled packages.
    
    @return: list<Package>
    '''
    return get_app_context()[APP_PACKAGING].get_disabled_packages()

def get_package(package_name):
    '''
    Returns the package by the given name.
    
    @param package_name: package name
    '''
    return get_app_context()[APP_PACKAGING].get_package(package_name)

def add_hook(hook):
    '''
    Sets the package manager hook.
    
    @param hook: hook instance
    '''
    
    return get_app_context()[APP_PACKAGING].add_hook(hook)
    
def get_hooks():
    '''
    Returns the package manager hook.
    
    @return: PackageManagerHook
    '''
    
    return get_app_context()[APP_PACKAGING].get_hooks()
