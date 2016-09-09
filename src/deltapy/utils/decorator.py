'''
Created on Sep 2, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

#TODO: collecting decorated functions.

def make_decorator(wrapper_class):
    '''
    Makes a decorator.
    
    Example:
    
    @make_decorator
    class trace:
        def __init__(self, *decorator_args, **decorator_kwargs):
            # Getting decorator parameters
            ...
            
        def wrapper(self, func, *args, **kwargs):
            # Do any things you want...
            return func(*args, **kwargs)
    
    @param wrapper_class: wrapper class
    @return: function
    '''
    def _decorator(*params, **options):
        
        func = None
        if len(params) > 0:
            func = params[0]
            
        if func:
            if func.__class__.__name__ not in ('instancemethod', 'function', 'cython_binding_builtin_function_or_method', 'builtin_function_or_method'):
                func = None
            else:
                params = params[1:]
            
        instance = wrapper_class(*params, **options)
        wrapper_func = instance.wrapper

        def new_f(*args, **kwargs):
            return wrapper_func(func, *args, **kwargs)
        
        def new_f_with_params(_func):
            def new_f(*args, **kwargs):
                return wrapper_func(_func, *args, **kwargs)
            new_f.__name__ = _func.__name__
            new_f.__doc__ = _func.__doc__
            return new_f
        
        if not func:
            return new_f_with_params
        
        new_f.__name__ = func.__name__
        new_f.__doc__ = func.__doc__

        return new_f

    return _decorator
