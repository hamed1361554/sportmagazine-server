'''
Created on Aug 10, 2009

@author: mohammadi
'''

from deltapy.locals import *

def get_logger(**kargs):
    '''
    Returns the associated logger.
    
    @param name: name of the logger
    @param others: other replacement logger names
    '''
    
    return get_app_context()[APP_LOGGING].get_logger(**kargs)

def reload_configs():
    '''
    Re-reads configs from the config file.
    '''
    return get_app_context()[APP_LOGGING].reload_configs()


def debug(msg, *args, **kwargs):
    get_app_context()[APP_LOGGING].debug(msg, *args, **kwargs)
    
def error(msg, *args, **kwargs):   
    get_app_context()[APP_LOGGING].error(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    get_app_context()[APP_LOGGING].exception(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    get_app_context()[APP_LOGGING].critical(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    get_app_context()[APP_LOGGING].info(msg, *args, **kwargs)    