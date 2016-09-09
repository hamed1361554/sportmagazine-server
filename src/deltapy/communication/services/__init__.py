'''
Created on Aug 10, 2009

@author: mohammadi
'''

from deltapy.locals import get_app_context, APP_COMMUNICATOR

def register_factory(type_name, factory):
    return get_app_context()[APP_COMMUNICATOR].register_factory(type_name, factory)

def get_listener(name):
    return get_app_context()[APP_COMMUNICATOR].get_listener(name)

def get_listener_params(name):
    return get_app_context()[APP_COMMUNICATOR].get_listener_params(name)

def get_default_listener():
    return get_app_context()[APP_COMMUNICATOR].get_default_listener()
    
def get_listeners():
    return get_app_context()[APP_COMMUNICATOR].get_listeners()

def start(config_store=None):
    return get_app_context()[APP_COMMUNICATOR].start(config_store)

def stop(force = False):
    return get_app_context()[APP_COMMUNICATOR].stop(force)

def create_proxy_by_ticket(ticket, user_name, **kwargs):
    return get_app_context()[APP_COMMUNICATOR].create_proxy_by_ticket(ticket, user_name, **kwargs)

def create_proxy(user_name, password, **kwargs):
    return get_app_context()[APP_COMMUNICATOR].create_proxy(user_name, password, **kwargs)

def add_hook(hook):
    return get_app_context()[APP_COMMUNICATOR].add_hook(hook)
        
def get_hooks():
    return get_app_context()[APP_COMMUNICATOR].get_hooks()
