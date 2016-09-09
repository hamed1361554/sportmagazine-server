'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.transaction.services as transaction

def transactional(*args, **options): 
    """
    
    @param auto_commit: auto commit flag
    @param pool_name: connection pool name
    """
    
    _auto_commit = options.get('auto_commit', True)
    _pool_name = options.get('pool_name', None)
    
    def transactional_decorator(old_func):
        """
            The decorate function.
        """

        def new_func(*args, **kwds):
            trx = None
            try:
                trx = transaction.begin(pool_name = _pool_name, 
                                        auto_commit = _auto_commit)
                result = old_func(*args, **kwds)
                if _auto_commit == True:
                    trx.commit()
                return result
            except:
                if trx:
                    trx.rollback()
                raise
        
        # Setting the new_function name...
        new_func.__name__ = old_func.__name__
        new_func.__module__ = old_func.__module__

        transactional_decorator.__name__ = old_func.__name__
        transactional_decorator.__module__ = old_func.__module__

        return new_func
    
    if len(args) > 0:
        old_func = args[0]
        if old_func.__class__.__name__ not in ('instancemethod',
                                               'function',
                                               'cython_binding_builtin_function_or_method',
                                               'cython_function_or_method',
                                               'builtin_function_or_method'):
            raise Exception('Invalid parameter for decorating function.')
        return transactional_decorator(old_func)

    return transactional_decorator
