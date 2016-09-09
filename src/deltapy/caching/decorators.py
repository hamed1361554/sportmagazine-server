'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

from threading import Lock

from deltapy.utils.decorator import make_decorator
from deltapy.caching.manager import CacheManagerException
import deltapy.caching.services as caching
from deltapy.caching.cache import CacheException

@make_decorator
class cache:
    '''
    Provides caching method result by method input parameters.
    '''
    
    # TODO: Getting category in caching methods
    def __init__(self, scavenger = None, name = None, category = 'functions', **cache_params):
        # Getting parameters
        self._scavenger = scavenger
        self._catogory = category
        self._cache = None
        self._lock = Lock()
        self._name = name
        self._cache_params = cache_params
        if self._name is not None and caching.exists(self._name):
            raise CacheManagerException('Cache [{name}] already exists.'.format(name=name))
        
    def _get_cache(self, old_func):
        if not self._cache:
            try:
                self._lock.acquire()
                if self._cache:
                    return self._cache
                if self._name is None:
                    self._name = "{module}.{func}".format(module = old_func.__module__, func = old_func.__name__)
                cache_type_name = None
                if 'cache_type_name' in self._cache_params:
                    cache_type_name = self._cache_params.pop('cache_type_name')
                self._cache = caching.get_cache(self._name, cache_type_name, **self._cache_params)
                self._cache.category = self._catogory
                self._cache.set_scavenger(self._scavenger)
            finally:
                self._lock.release()
                
        return self._cache
       
    def wrapper(self, func, *args, **kwargs):
        '''
        Wraps the function.
        
        @param func: function
        @return: depends on function
        '''
        
        #t = time.time()
        #logger = logging.get_logger()
        #logger.debug('Cache[%s]...' % func)

        _cache = self._get_cache(func)
        
        # Creating input parameters key
        # TODO: fix creating cache key 
        key = str(args) + str(kwargs)
        
        try:
            # Looking in cache
            if _cache.has_key(key):
                #logger.debug('Reading from cache[%s] in %f seconds.' % (func, time.time() - t))
                return self._cache[key]
        except CacheException:
            pass
        
        # Executing function, If key is not in cache
        result = func(*args, **kwargs)
        
        # Updating cache
        _cache[key] = result
        
        #logger.debug('Cache[%s] executing function in %f seconds.' % (func, time.time() - t))

        # Returning the result 
        return result

@make_decorator
class cache_reset:
    '''
    Provides caching method result by method input parameters.
    '''
    
    # TODO: Getting category in caching methods
    def __init__(self, name):
        # Getting parameters
        self._name = name
        
    def wrapper(self, func, *args, **kwargs):
        '''
        Wraps the function.
        
        @param func: function
        @return: depends on function
        '''
        
        # Calling decorated function
        result = func(*args, **kwargs)

        # Reseting cache
        caching.reset_cache(self._name)

        # Returning the result 
        return result
        
#@make_decorator
#class cache_:
#    '''
#    Provides caching method result by method input parameters.
#    '''
#    def __init__(self, scavenger = None):
#        # Getting parameters
#        weeks = kwargs.get('weeks', 0)
#        days = kwargs.get('days', 0)
#        hours = kwargs.get('hours', 0)
#        minutes = kwargs.get('minutes', 0)
#        seconds = kwargs.get('seconds', 0)
#        
#        self.lifetime = timedelta(weeks = weeks,
#                                  days = days,
#                                  hours = hours,
#                                  minutes = minutes,
#                                  seconds = seconds)
#        
#        self._cache = None
#        
#    def __get_cache__(self, old_func):
#        if not self._cache:
#            self._cache = caching.get_cache("%s.%s" % (old_func.__module__, 
#                                                       old_func.__name__))
#            self._cache.category = 'functions'
#            self._cache.set_lifetime(self.lifetime)
#        return self._cache
#       
#    def wrapper(self, func, *args, **kwargs):
#        '''
#        Wraps the function.
#        
#        @param func: function
#        @return: depends on function
#        '''
#        
#        #t = time.time()
#        #logger = logging.get_logger()
#        #logger.debug('Cache[%s]...' % func)
#
#        _cache = self.__get_cache__(func)
#        
#        # Creating input parameters key 
#        key = args + tuple(kwargs)
#        
#        # Looking in cache
#        if _cache.has_key(key):
#            #logger.debug('Reading from cache[%s] in %f seconds.' % (func, time.time() - t))
#            return self._cache[key]
#        
#        # Executing function, If key is not in cache
#        result = func(*args, **kwargs)
#        
#        # Updating cache
#        _cache[key] = result
#        
#        #logger.debug('Cache[%s] executing function in %f seconds.' % (func, time.time() - t))
#
#        # Returning the result 
#        return result
