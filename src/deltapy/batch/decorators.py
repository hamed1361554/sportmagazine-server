'''
Created on Dec 26, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.batch.services as batch

def register_batch_process_unit(process_unit_id, 
                                *constructor_args,
                                **constructor_kwargs):
    '''
    Registers a batch unit processor.
    
    @param process_unit_id: process unit ID
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
        instance = cls(process_unit_id,
                       *constructor_args,
                       **constructor_kwargs)
        
        # Registering the instance in batch processor
        batch.add_process_unit(instance)
        
        def wrapper(*args, **kwds):
            '''
            Wraps the class.
            
            @return: object(the class instance)
            '''
            return instance
        
        return wrapper
    
    return decorator
