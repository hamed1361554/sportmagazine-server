'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

from deltapy.locals import *

def load_pools():
    return get_app_context()[APP_DATABASE].make_defined_pools()

def get_pools():
    return get_app_context()[APP_DATABASE].get_pools()

def open(pool_name = None):
    return get_app_context()[APP_DATABASE].open(pool_name)

def close(store):
    get_app_context()[APP_DATABASE].close(store)

def add_pool(pool):
    return get_app_context()[APP_DATABASE].add_pool(pool)

def reset_pools():
    return get_app_context()[APP_DATABASE].reset_pools()

