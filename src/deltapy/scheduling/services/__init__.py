'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

from deltapy.locals import *

def create_task(name, 
                start_time, 
                calc_next_time_func, 
                func, 
                **func_kargs):
    """
    Returns created task object.

    Arguments:
    @param name                - Name of task.
    @param start_time          - First time for task to run
    @param calc_next_time_func - Function to calculate the time of next run, 
                                  gets one argument, the last run time as a datetime.
                                  Returns None when task should no longer be run
    @param func                - A function to run
    @param **func_kargs        - Parameters of specified function.
    """
    return get_app_context()[APP_SCHEDULING].create_task(name, 
                                                            start_time, 
                                                            calc_next_time_func, 
                                                            func, 
                                                            **func_kargs)
    
def schedule(name, 
             start_time, 
             calc_next_time_func, 
             func, 
             expire_time = None,
             before_run = None,
             after_run = None,
             retry_count = 0, 
             **func_args):
    """
    Returns created task object.

    Arguments:
    @param name                - Name of task.
    @param start_time          - First time for task to run
    @param calc_next_time_func - Function to calculate the time of next run, 
                                  gets one argument, the last run time as a datetime.
                                  Returns None when task should no longer be run
    @param func                - A function to run.
    @param retry_count         - Number of tries.
    @param expire_time         - Expire date of task.
    @param before_run          - This function will be run before executing task.
    @param after_run           - This function will be run after executing task.
    @param **func_kargs        - Parameters of specified function.
    """
    return get_app_context()[APP_SCHEDULING].schedule(name, 
                                                      start_time, 
                                                      calc_next_time_func, 
                                                      func, 
                                                      expire_time = None,
                                                      before_run = None,
                                                      after_run = None,
                                                      retry_count = 0, 
                                                      **func_args)

def get_tasks():
    return get_app_context()[APP_SCHEDULING].tasks

def get_task(task_id):
    return get_app_context()[APP_SCHEDULING].tasks[task_id]

def schedule_task(task):
    return get_app_context()[APP_SCHEDULING].schedule_task(task)

def drop(task_id):
    return get_app_context()[APP_SCHEDULING].drop(task_id)        

def halt():
    get_app_context()[APP_SCHEDULING].halt()
        
def run():
    get_app_context()[APP_SCHEDULING].run()