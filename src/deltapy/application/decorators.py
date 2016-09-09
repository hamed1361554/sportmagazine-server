'''
Created on Oct 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.application.services as application

def register(id, *constructor_args, **constructor_kwargs):
    '''
    Registers a component in the application context.
    
    @param id: component ID
    @param *constructor_args: arguments which is required for creating an instance
    @param **constructor_kwargs: keyword arguments which is required for creating an instance
    
    @return: function
    '''
    
    def decorator(cls):
        '''
        Decorates the given class and registers a instance of this class.
        
        @param cls: component class
        @return: function
        '''
        
        # Creating an instance of class
        instance = cls(*constructor_args,**constructor_kwargs)
        
        # Registering the instance in application context
        application.register_component(id, instance)
        
        return cls
    
    return decorator
