'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

import deltapy.logging.services as logging
import operator
import datetime
import thread
from threading import Thread, Event, Lock
from deltapy.utils.uniqueid import get_uuid
import time

class Task: 
    '''
    Task class.
    '''
    
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    WAIT = 'wait'
    RUNNING = 'running'
    HALTED = 'halted'

    PRIORITY_LOW = -1
    PRIORITY_NORMAL = 0
    PRIORITY_HIGH = 1
    PRIORITY_VERY_HIGH = 2
             
    logger = logging.get_logger(name = 'scheduler')
    
    def __init__(self, 
                 name,
                 start_time, 
                 calc_next_time_func, 
                 action,
                 **kargs):
        """
        Initialize a Task.
        
        @param name: Name of task.
        @param start_time: First time for task to run
        @param calc_next_time_func: Function to calculate the time of next run, 
                              gets one argument, the last run time as a datetime.
                              Returns None when task should no longer be run
        @param action: A function to run
        
        """
       
        self.name = name
        self.start_time = start_time                
        self.scheduled_time = self.start_time
        self.calc_next_time_func = calc_next_time_func
        self.action = action
        self.action_kargs = kargs
        self.retry_count = 0
        self.expire_time = None
        self.exec_count = 0
        self.exec_count_limit = 0
        self.priority = Task.PRIORITY_NORMAL
        self.halt_flag = Event()
        self.task_id = get_uuid()
        self.status = Task.WAIT
        self.last_exec_time = None
        self.last_error = None
        self.before_run = lambda task : None
        self.after_run = lambda task : None
        while self.scheduled_time < datetime.datetime.now():
            self.scheduled_time = self.calc_next_time_func(self.scheduled_time)
        
    def run(self):
        
        self.logger.debug("Running Task [%s] , at: %s" % (self.name, 
                                                          datetime.datetime.now()))

        if self.before_run:
            self.before_run(self)
        
        retry_count = self.retry_count
        
        if not self.halt_flag.isSet():
            while retry_count + 1 > 0:
                try:
                    self.last_exec_time = time.time()
                    self.action(**self.action_kargs)
                    self.status = Task.SUCCEEDED
                    break
                except Exception, error:
                    self.last_error = error
                    self.status = Task.FAILED
                    retry_count -= 1
                    
        if self.after_run:
            self.after_run(self)
        
        self.exec_count += 1   
        
        if self.calc_next_time_func:
            self.scheduled_time = self.calc_next_time_func(self.scheduled_time)

        self.logger.debug("Scheduled next run of %s for: %s" % (self.name, 
                                                                self.scheduled_time,))            
            
    def halt(self):
        self.halt_flag.set()
        self.status= Task.HALTED
    
    def get_id(self):
        return self.task_id

class TaskExecutor:
    logger = logging.get_logger(name = 'scheduler')
    
    def __init__(self, on_running_task):
        self.running_threads = {}
        self.on_running_task = on_running_task
        self.tasks_lock = Lock()
        
    def __run_task__(self,task):        
        try:
            self.tasks_lock.acquire()
            if self.on_running_task:
                self.on_running_task(task)        
            self.running_threads[task.task_id]= task        
            task.status = Task.RUNNING
            task.run()
            self.running_threads.pop(task.task_id)
        except Exception, e:
            TaskExecutor.logger.exception(e)
            raise
        finally:
            self.tasks_lock.release()
            
    def execute(self,task):        
        if not self.running_threads.has_key(task.task_id):
            thread.start_new_thread(self.__run_task__, (task,))
              
class Scheduler(Thread):
    """
    Provides some functions for scheduling tasks.
    """
    
    logger = logging.get_logger(name = 'scheduler')
    
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)        

        self.tasks = {}        
        self.tasks_lock = Lock()
        self.halt_flag = Event()
        self.nonempty = Event()     
        self.on_running_task = lambda t:None   
    
    def create_task(self, 
                    name, 
                    start_time, 
                    calc_next_time_func, 
                    func, 
                    **func_kargs):
        task = Task(name, 
                    start_time, 
                    calc_next_time_func,
                    func,
                    **func_kargs)
        return task
    
    def schedule(self, 
                 name, 
                 start_time, 
                 calc_next_time_func, 
                 func, 
                 expire_time = None,
                 before_run = None,
                 after_run = None,
                 retry_count = 0, 
                 **func_args):
        
        task = Task(name, 
                    start_time, 
                    calc_next_time_func, 
                    func, 
                    **func_args)
        
        #task.priority = priority
        task.expire_time = expire_time
        task.retry_count = retry_count
        task.before_run = before_run
        task.after_run = after_run  
        
        return self.schedule_task(task)
    
    def schedule_task(self, task):
        
        receipt = task.get_id()
        try:
            self.tasks_lock.acquire()
            self.tasks[receipt] = task
            self.nonempty.set()
        finally:
            self.tasks_lock.release()
        
        return receipt
    
    def drop(self, task_receipt):
        try:
            self.tasks_lock.acquire()
            self.tasks[task_receipt].halt()
            del self.tasks[task_receipt]
            if len(self.tasks)==0:
                self.nonempty.clear()
        except KeyError:
            self.logger.error('Invalid task receipt: %s' % (task_receipt,))
        finally:
            self.tasks_lock.release()
        
    def halt(self):
        self.halt_flag.set()
        # Drop all active tasks
        map(self.drop, self.tasks.keys())
        # Exit the thread to kill the scheduler
        
    def __find_next_tasks__(self):
        try:
            self.tasks_lock.acquire()
            receipts = []
            
            items = self.tasks.items()
            
            by_time = lambda x: operator.getitem(x, 1).scheduled_time
                        
            items.sort(key = by_time)      
               
            for index in xrange(len(self.tasks)):
                receipt = items[index][0]
                task = self.tasks[receipt]
                task_time = task.scheduled_time
                now = datetime.datetime.now()
                time_to_wait = task_time - now
                secs_to_wait = 0.
                secs_to_wait = time_to_wait.seconds
                if secs_to_wait <= 0 and secs_to_wait >= -5:
                    if not task.status in (Task.RUNNING, Task.HALTED):
                        if task.scheduled_time >= datetime.datetime.now():
                            receipts.append(receipt)

            return receipts
                    
        finally:
            self.tasks_lock.release()
        
    def run(self):
        task_executor = TaskExecutor(self.on_running_task)
        
        while True:
            # Waiting for a second
            time.sleep(1)
           
            receipts = self.__find_next_tasks__()
            
            ignore_task = False
            
            for receipt in receipts:
                if receipt != None:
                    #self.halt_flag.wait(secs_to_wait)
                    ignore_task = False
                    try:
                        try:
                            self.tasks_lock.acquire()
                            task = self.tasks[receipt]                                              
    
                            if task.exec_count_limit > 0 and  task.exec_count > task.exec_count_limit:
                                self.logger.debug("Task %s execution count exceeded." % (task.name,))
                                self.tasks.pop(receipt)
                                ignore_task = True
                                    
                            #checking task expiration time                        
                            if task.expire_time and task.expire_time < datetime.datetime.now():
                                self.logger.debug("Task %s expired" % (task.name,))
                                self.tasks.pop(receipt)
                                ignore_task = True
                            
                            if not ignore_task:
                                task_executor.execute(task)
                                #task.run()                         
    
                        finally:
                            self.tasks_lock.release()
                    except Exception, e:
                        self.logger.exception(e)
                        self.logger.debug( self.tasks )
                else:
                    self.nonempty.wait()
