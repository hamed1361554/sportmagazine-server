'''
Created on Aug 29, 2009

@author: mohammadi, vesal
'''

from deltapy.locals import *

def begin_root(**kargs):
    '''
    Begins a transaction and return it.
    
    @param auto_commit: auto commit flag
    @param pool_name: connection pool name
    
    @return: Transaction
    ''' 
    
    kargs.update(is_root=True)
    return get_app_context()[APP_TRANSACTION].begin(**kargs)

def begin(**kargs):
    '''
    Begins a transaction and return it.
    
    @param auto_commit: auto commit flag
    @param pool_name: connection pool name
    @param is_root: root transaction flag
    
    @return: Transaction
    ''' 
    return get_app_context()[APP_TRANSACTION].begin(**kargs)
    
def commit(tx):
    return get_app_context()[APP_TRANSACTION].commit(tx)

def rollback(tx):
    return get_app_context()[APP_TRANSACTION].rollback(tx)

def tpc_begin():
    return get_app_context()[APP_TRANSACTION].tpc_begin()      

def get_current_transaction(pool_name = None):
    return get_app_context()[APP_TRANSACTION].get_current_transaction(pool_name)

def get_current_transaction_store():
    trx = get_app_context()[APP_TRANSACTION].get_current_transaction()
    if not trx:
        raise Exception('There is not corresponded transaction.')
    return trx.get_connection()

def get_store(trx):
    return trx.get_connection()

def get_store_by_pool(pool_name):
    trx = get_app_context()[APP_TRANSACTION].get_current_transaction(pool_name)
    if not trx:
        raise Exception('There is not corresponded transaction.')
    return trx.get_connection()

def get_database_manager():
    return get_app_context()[APP_TRANSACTION].get_database_manager()

