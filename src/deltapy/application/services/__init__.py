'''
Created on Nov 23, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
from deltapy.locals import get_app
import deltapy.config.services as config

def get_name():
    '''
    Returns application's name.
    @return: str
    '''
    return get_app().get_name()

def get_instance_name():
    '''
    Returns application's instance name.
    
    @return: str
    '''
    return get_app().get_instance_name()

def get_full_name():
    '''
    Returns application's full name.
    
    @return: str
    '''
    return get_app().get_full_name()
    
def enlist_app(app_name, 
               instance_name, 
               user_name, 
               ticket, 
               listener_params):
    '''
    Enlists an application.
    
    @param app_name: application name
    @param instance_name: application instance name
    @param user_name: user name
    @param ticket: ticket of the user
    @param listener_params: parameters of the listener
    '''
    return get_app().enlist_app(app_name,
                                instance_name, 
                                user_name, 
                                ticket, 
                                listener_params)

def delist_app(app_name, 
               instance_name):
    """
    Delists an application into current application as child.
    
    @param app_name: name of child application.
    @param instance_name: application instance name. 
    """

    return get_app().delist_app(app_name, 
                                instance_name)
def register_component(name, instance):
    '''
    Registers a component in application context.
    
    @param name: component name
    @param instance: a instance of the component
    '''
    
    return get_app().register_component(name, instance)
    
def unregister_component(name):
    '''
    Unregisters the component from the application context by the given name.
    
    @param name: component name 
    '''
    
    return get_app().unregister_component(name)
    
def get_component(name):
    '''
    Returns the component using the given name.
    
    @param name: component name
    @return: object
    '''
    
    return get_app().get_component(name)

def introduce():
    '''
    Introduces the application.
    '''               
    return get_app().introduce()

def get_real_path(environmental_path):
    '''
    Returns replaced path with environmental paths
    
    for example :
        $DELTA_HOME/test.db -> /opt/deltapy/test.db
    
    @param path: environmental path
    @return: str
    '''
    
    result = environmental_path
    
    config_store = config.get_app_config_store()
    if config_store.has_section('path'):
        paths = config_store.get_section_data('path')
        for pth in paths:
            rpath = '$%s%s' % (pth, os.path.sep)
            value = '%s%s' % (paths[pth], os.path.sep)
            result = result.replace(rpath.upper(), value)
            result = result.replace(rpath.lower(), value)
    
    return result

def get_context():
    '''
    Returns application context.
    '''
    
    return get_app().get_context()

def get_options():
    '''
    Returns applications options.
    
    @return: {}
    '''

    return get_app().get_options()

def get_default_settings_folder_name():
    '''
    Returns default settings folder name.
    
    @return: str
    '''
    
    return get_app().get_default_settings_folder_name()

def get_application_dir():
    '''
    Returns application running path.
    
    @rtype: str
    '''

    return get_app().get_application_dir()

