'''
Created on Oct 12, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import deltapy.caching.services as caching
from deltapy.utils.decorator import make_decorator
import deltapy.logging.services as logging
import time

logger = logging.get_logger()

@make_decorator
class trace:
    '''
    Provides caching method result by method input parameters.
    '''
    
    logger = logging.get_logger()
    
    def __init__(self, *args, **options):
        pass

    def wrapper(self, func, *args, **kwargs):
        '''
        Wraps the function.
        
        @param func: function
        @return: depends on function
        '''
        
        start_time = time.time()
        try:
            # Returning the result 
            return func(*args, **kwargs)
        except Exception, error:
            self.logger.debug('Error on executing function[%s.%s]:%s' % (func.__module__, 
                                                                          func.__name__, 
                                                                          error))
            raise
        finally:
            elapsed_time = time.time() - start_time
            self.logger.debug('Function[%s.%s] executed in %f seconds.' % (func.__module__,
                                                                             func.__name__, 
                                                                             elapsed_time))

