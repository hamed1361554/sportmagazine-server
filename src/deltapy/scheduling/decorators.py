'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

import deltapy.scheduling.services as scheduling

def schedule(name, 
             start_time, 
             calc_next_time_func, 
             **options): 
    """
    Creates a task and adds it to scheduler.
    
    @param name: Task name
    @param start_time: Task start time
    @param calc_next_time_func: Function for calculating next execution time
    @param options: expire_time, before_run, after_run, retry_count

    Example
        @schedule('task_1', 
                  datetime.datetime.now(), 
                  every_x_minute(30), 
                  expire_time = datetime.datetime(2009, 1, 1))
        def func():
            ...
    """
    
    expire_time = None
    if options and options.has_key('expire_time'):
        expire_time = options['expire_time']

    before_run = None
    if options and options.has_key('before_run'):
        before_run = options['before_run']

    after_run = None
    if options and options.has_key('after_run'):
        after_run = options['after_run']

    retry_count = 0
    if options and options.has_key('retry_count'):
        retry_count = options['retry_count']
    
    def schedule_decorator(old_func):
        """
            The decorate function.
        """

        def new_func(*args, **kwds):
            
            # Decorating old function
            return old_func(*args, **kwds)
        
        # Setting the new_function name...
        new_func.__name__ = old_func.__name__
        new_func.__module__ = old_func.__module__

        schedule_decorator.__name__ = old_func.__name__
        schedule_decorator.__module__ = old_func.__module__

        # Creating a task and adding it 
        scheduling.schedule(name, 
                            start_time, 
                            calc_next_time_func, 
                            new_func, 
                            expire_time, 
                            before_run, 
                            after_run, 
                            retry_count)

        return old_func

    return schedule_decorator
