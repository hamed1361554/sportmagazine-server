'''
Created on Nov 6, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import traceback
import time

from deltapy.core import DeltaObject, DeltaException, DynamicObject
from deltapy.batch.parallel import ParallelExecutor
import deltapy.config.services as config
import deltapy.logging.services as logging


class BatchProcessManagerException(DeltaException):
    '''
    For handling batch process manager errors.
    '''

class BatchProcessManager(DeltaObject):
    '''
    Provides management on process units.
    '''
    
    logger = logging.get_logger(name = 'batch')
    
    def __init__(self):
        DeltaObject.__init__(self)
        self.__process_units = {}

    def __get_process_unit_data__(self, name):
        '''
        Returns specific batch processor.
        
        @param name: name of batch processor.
        '''
        try:
            return self.__process_units[name]
        except KeyError:
            raise BatchProcessManagerException("Process unit[%s] not found." % 
                                               name)
        
    def __get_parallel_executor__(self, process_unit_name):
        '''
        Returns parallel executor of a process unit.
        
        @param process_unit_name: process unit name
        @return: ParallelExecutor
        '''
        
        # Getting process unit data
        data = self.__get_process_unit_data__(process_unit_name)
        
        # data is a tuple of (process_unit, parallel_executor)
        return data[1]
        
    def get_process_units(self, status = None):
        '''
        Returns all process units by the given status
        
        @param status: status
            'Stopped'
            'InProgress'
            'Suspended'
            'Completed'
            'Ready'
            'NotReady'
            'Failed'
        @return: [ProcessUnit]
        '''
        
        process_units = []
        for process_unit, parallel_executor in self.__process_units.values():
            #Commented because batch.list command returned Empty Result.
            #if parallel_executor is not None:
            if not status or parallel_executor.get_status() == status:
                process_units.append(process_unit)
        return  process_units

    def get_process_unit(self, name):
        '''
        Returns specific process unit.
        
        @param name: name of process unit.
        @return: ProcessUnit
        '''
        
        # Getting process unit data
        data = self.__get_process_unit_data__(name)
        
        # data is a tuple of (process_unit, parallel_executor)
        return data[0]
        
    def add_process_unit(self, process_unit, **options):
        '''
        Adds a process unit to batch processor.
        If a process unit with the same ID exists,
        it will override it.

        @param process_unit: process unit instance
        '''
        
        # Getting process unit name
        name = process_unit.get_name()
        
        # Adding process unit data as a tuple 
        # (process unit instance, parallel executor instance)
        self.__process_units[name] = (process_unit, None)
        
    def __before_start_process_unit__(self, 
                                      process_unit,
                                      parallel_executor, 
                                      thread_count, 
                                      params):
        # TODO: BatchProcessManager start hooks
        # Calling process unit to creating it's chunks
        
        process_unit_name = process_unit.get_name()
        
        BatchProcessManager.logger.info("Process unit[%s] started it's chunks creation." % process_unit_name)
        chunks = process_unit.create_chunks()            
        BatchProcessManager.logger.info("Process unit[%s] finished it's chunks creation." % process_unit_name)
                    
        if chunks is None or len(chunks) == 0:
            message = _('Can not start process unit[{unit_name}] without chunks.')
            process_unit.get_message_stream().error(message.format(unit_name = process_unit_name))
            raise BatchProcessManagerException(message.format(unit_name = process_unit_name))
        
        message = _('Process unit[{unit_name}] will be started by {chunk_count} chunks.')
        BatchProcessManager.logger.info(message.format(unit_name = process_unit_name, 
                                                       chunk_count = len(chunks))) 

        # Adding created chunks as parallel executor parameters
        parallel_executor.add_parameters(chunks)
        
    def __after_finished_process_unit__(self,
                                        process_unit):
        process_unit.done()
        BatchProcessManager.logger.info('Process unit[%s] completed.' % process_unit.get_name())
        process_unit.get_message_stream().info('Process unit[%s] completed.' % process_unit.get_name())
        
        # TODO: BatchProcessManager complete hooks
    def __on_proccess_unit_failed__(self, process_unit, error, error_trace):
        try:
            BatchProcessManager.logger.error('Process unit[%s] failed:%s.' % (process_unit.get_name(), error_trace))
            process_unit.get_message_stream().error('Process unit[%s] failed:%s.' % (process_unit.get_name(), error_trace))
            process_unit.failed(error)
        except:
            BatchProcessManager.logger.error('Process unit[%s] failed:%s.' % (process_unit.get_name(), traceback.format_exc()))
            process_unit.get_message_stream().error('Process unit[%s] failed:%s.' % (process_unit.get_name(), traceback.format_exc()))

    def __before_start_process_unit_chunk__(self, 
                                            process_unit,
                                            chunk):
        BatchProcessManager.logger.info('Process unit[%s] is going to start chunk[%s].' % (process_unit.get_name(), chunk))
        process_unit.get_message_stream().info('Process unit[%s] is going to start chunk[%s].' % (process_unit.get_name(), chunk))

    def __after_complete_process_unit_chunk__(self, 
                                              process_unit,
                                              chunk,
                                              result): 
        BatchProcessManager.logger.info('Process unit[%s] finished chunk[%s].' % (process_unit.get_name(), chunk))
        process_unit.get_message_stream().info('Process unit[%s] finished chunk[%s].' % (process_unit.get_name(), chunk))        

    def __on_process_unit_chunk_failed__(self, 
                                         process_unit,
                                         chunk,
                                         error):
        error_detail = traceback.format_exc()        
        BatchProcessManager.logger.error('Process unit[%s] failed on chunk[%s] : %s\n Trace: %s.' % (process_unit.get_name(), chunk, error, error_detail))
        process_unit.get_message_stream().error('Process unit[%s] failed on chunk[%s] : %s\n Trace: %s.' % (process_unit.get_name(), chunk, error, error_detail))
    
    def __get_process_unit_config__(self, name):
        '''
        Returns process unit configuration from batch.config file.
        
        @param name: process unit name
        '''
        
        # Getting batch configuration store
        config_store = config.get_app_config_store('batch')
        
        # Getting default parameters from configuration file.
        if config_store.has_section(name):
            return config_store.get_section_data(name)
        return DynamicObject(thread_count=1)
        
    def start(self, 
              process_unit_name, 
              **options):
        '''
        Starts a process unit.
        
        @param process_unit_name: process unit name
        '''

        BatchProcessManager.logger.info('Loading process unit[%s]' % process_unit_name)
        process_unit = None
        try:
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            if parallel_executor is not None and not parallel_executor.can_run():
                raise BatchProcessManagerException('Process unit[%s] is %s.' % (process_unit_name, self.get_status(process_unit_name)))
            
            # Getting process unit default parameters
            params = self.__get_process_unit_config__(process_unit_name)
            
            # Checking process unit enable flag 
            enabled = bool(params.get('enabled', True))
            
            #TODO: it should be add to base of process unit and set_enable command
            # should be created.
            if enabled == False:
                raise BatchProcessManagerException('Process unit[%s] is disabled.' % (process_unit_name))                
            
            # Updating default parameters with given options
            params.update(options)
            
            # Getting process unit instance
            process_unit = self.get_process_unit(process_unit_name)

            # Configuring the process unit with updated parameters
            process_unit.configure(**params)
            
            # Getting joining information
            joined_groups = process_unit.get_joined_groups()
            joined_units = process_unit.get_joined_units()
            
            # Joining to groups and units
            for joined_group in joined_groups:
                self.join_to_group(joined_group)
            for joined_unit in joined_units:
                self.join(joined_unit)
            
            # Getting thread count
            thread_count = int(params.get('thread_count', 1))

            # Creating a new parallel executor instance
            parallel_executor = ParallelExecutor(process_unit.get_name(), 
                                                 process_unit.process,
                                                 thread_count)
            
            
            # Creating event handler functions
            before_start = lambda : self.__before_start_process_unit__(process_unit, parallel_executor, thread_count, params)
            after_finished = lambda : self.__after_finished_process_unit__(process_unit)
            on_failed = lambda error, error_trace: self.__on_proccess_unit_failed__(process_unit, error, error_trace)
            before_start_task = lambda chunk: self.__before_start_process_unit_chunk__(process_unit, chunk)
            after_complete_task = lambda chunk, result: self.__after_complete_process_unit_chunk__(process_unit, chunk, result)
            on_task_failed = lambda chunk, error: self.__on_process_unit_chunk_failed__(process_unit, chunk, error)
            
            # Setting parallel executor event handler functions
            parallel_executor.set_before_start(before_start)
            parallel_executor.set_after_finished(after_finished)
            parallel_executor.set_on_failed(on_failed)
            parallel_executor.set_before_start_task(before_start_task)
            parallel_executor.set_after_complete_task(after_complete_task)
            parallel_executor.set_on_task_failed(on_task_failed)

            # Updating process unit data with created new parallel executor
            self.__process_units[process_unit_name] = (process_unit, 
                                                       parallel_executor)

            BatchProcessManager.logger.info('Process unit[%s] is creating chunks, its may takes a several minutes...' % process_unit_name)

            # Truncating process unit message stream 
            process_unit.get_message_stream().truncate()
            process_unit.get_message_stream().info('Started with parameters[%s]' % params)

            # Starting parallel executor to running batch operation
            parallel_executor.start()

            BatchProcessManager.logger.info('Process unit[%s] started with parameters[%s].' % 
                                            (process_unit_name, 
                                             params))
            
        except Exception, error:
            message = 'Starting process unit[{0}] failed:{1}' 
            BatchProcessManager.logger.error(message.format(process_unit_name, traceback.format_exc()))
            if process_unit is not None:
                message = 'Starting failed:{0}'
                process_unit.get_message_stream().error(message.format(str(error)))
                process_unit.failed(error)
            raise
        
    def join(self, process_unit_name):
        '''
        Joins to a process unit.
        
        @param process_unit_name: process unit name
        '''
        
        try:
            BatchProcessManager.logger.info('Process unit[%s] is joined.' % process_unit_name)
            
            # Getting process unit's parallel executor
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            if parallel_executor:
                # Waiting until parallel executor is running.  
                parallel_executor.join()
        except Exception:
            BatchProcessManager.logger.error('Joining to process unit[%s] failed:%s'% 
                                             (process_unit_name, traceback.format_exc()))
            raise
    
    def join_to_group(self, name):
        '''
        Joins to a group of process units.
        
        @param name: process units group
        '''

        try:
            BatchProcessManager.logger.info('Process unit group[%s] is joined.' % name)
            
            # Making a loop on all process units and their parallel executor
            for process_unit, parallel_executor in self.__process_units.values():
                if process_unit.get_group() == name:
                    if parallel_executor:
                        parallel_executor.join()
                        
        except Exception:
            BatchProcessManager.logger.error('Joining to process unit group[%s] failed:%s' % 
                                             (name, traceback.format_exc()))
            raise
                
    def resize(self, process_unit_name, thread_count):
        '''
        Resizes thread count of a process unit.
        
        @param process_unit_name: process unit name
        @param thread_count: thread count
        '''

        process_unit = None
        
        try:
            BatchProcessManager.logger.info('Resizing process unit[%s] to %d threads' % 
                                            (process_unit_name, thread_count))
    
            process_unit = self.get_process_unit(process_unit_name)
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            if parallel_executor:
                parallel_executor.resize(thread_count)
    
            BatchProcessManager.logger.info('Process unit[%s] resized to %d threads.' % 
                                            (process_unit_name, thread_count))
            
            process_unit.get_message_stream().info('Resized to %d threads.' % thread_count)

        except Exception, error:
            BatchProcessManager.logger.error('Resizing process unit[%s] failed:%s' % 
                                             (process_unit_name, traceback.format_exc()))
            
            if process_unit:
                process_unit.get_message_stream().error('Resizing is failed:%s.' % str(error))
                
            raise
        
    def stop(self, process_unit_name):
        '''
        Stops the process unit.
        
        @param process_unit_name: process unit name
        '''

        process_unit = None
        
        try:
            BatchProcessManager.logger.info('Stopping process unit[%s]' % 
                                            (process_unit_name))
            
            process_unit = self.get_process_unit(process_unit_name)
            process_unit.stopping()
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            if parallel_executor:
                parallel_executor.stop()

            BatchProcessManager.logger.info('Process unit[%s] stopped.' % 
                                            (process_unit_name))
            
            process_unit.get_message_stream().info('Stopped.')

        except Exception, error:
            BatchProcessManager.logger.error('Stopping process unit[%s] failed:%s' % 
                                             (process_unit_name, traceback.format_exc()))
            process_unit.get_message_stream().error('Stop failed:%s' % str(error))
            raise
        
    def suspend(self, process_unit_name):
        '''
        Suspends the process unit.
        
        @param process_unit_name: process unit name
        '''
        
        process_unit = None
        
        try:
            BatchProcessManager.logger.info('Suspending process unit[%s]' % 
                                            (process_unit_name))
            
            process_unit = self.get_process_unit(process_unit_name)
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            if not parallel_executor:
                raise BatchProcessManagerException("Process unit[%s] is not running.")
            parallel_executor.suspend()

            BatchProcessManager.logger.info('process unit[%s] suspended.' % 
                                            (process_unit_name))
            process_unit.get_message_stream().info('Suspended.')
        except Exception, error:
            BatchProcessManager.logger.error('Suspending process unit[%s] failed:%s' % 
                                             (process_unit_name, traceback.format_exc()))
            process_unit.get_message_stream().error('Suspend failed:%s.' % str(error))
            raise
        
        

    def resume(self, process_unit_name):
        '''
        Resumes the process unit.
        
        @param process_unit_name: process unit name
        '''
        
        process_unit = None

        try:
            BatchProcessManager.logger.info('Resuming process unit[%s]' % 
                                            (process_unit_name))
            process_unit = self.get_process_unit(process_unit_name)
            parallel_executor = \
                self.__get_parallel_executor__(process_unit_name)
            if not parallel_executor:
                raise BatchProcessManagerException("Process unit[%s] is not running.")
            parallel_executor.resume()
            BatchProcessManager.logger.info('Process unit[%s] resumed.' % 
                                            (process_unit_name))
            process_unit.get_message_stream().info('Resumed.')
        except Exception, error:
            BatchProcessManager.logger.error('Resuming process unit[%s] failed:%s' %
                                             (process_unit_name, traceback.format_exc()))
            process_unit.get_message_stream().error('Resume failed:%s.' % str(error))
            raise
        
    def get_status(self, process_unit_name):
        '''
        Returns process unit status.
        
        @param process_unit_name: process unit name
        '''
        
        parallel_executor = self.__get_parallel_executor__(process_unit_name)
        if parallel_executor:
            BatchProcessManager.logger.info('Process unit[%s] is %s.' % 
                                            (process_unit_name, 
                                             parallel_executor.get_status()))
            return parallel_executor.get_status()
    
    def is_completed(self, process_unit_name):
        '''
        Returns True if the process unit is completed, otherwise False
        
        @param process_unit_name: process unit name
        '''
        
        parallel_executor = self.__get_parallel_executor__(process_unit_name)
        
        if parallel_executor is not None:
            return parallel_executor.is_completed()
        else:
            return False
    
    def get_process_unit_info(self, process_unit_name):
        '''
        Returns process unit information.
        
        @param process_unit_name: process unit name
        @return: DynamicObject<>
        '''

        try:
            BatchProcessManager.logger.info('Getting process unit[%s] information' % 
                                            (process_unit_name))

            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            process_unit = self.get_process_unit(process_unit_name)
            return ProcessUnitInformation(process_unit, parallel_executor=parallel_executor)
        except Exception:
            BatchProcessManager.logger.error('Getting process unit[%s] information failed:%s' %
                                             (process_unit_name, traceback.format_exc()))
            raise
    
    def get_process_unit_performance(self, process_unit_name):
        '''
        Returns particular process unit information.
        
        @param process_unit_name: process unit name
        @return: float
        '''

        try:
            process_unit = self.get_process_unit(process_unit_name)
            parallel_executor = self.__get_parallel_executor__(process_unit_name)
            
            if parallel_executor is not None:
                #raise Exception('Parallel executor does not exists for process unit [%s]'% process_unit.get_name())
                start_time, end_time = parallel_executor.get_running_times()
                completed_chunks = parallel_executor.get_compeleted_count()
                
                performance = process_unit.calculate_performance(start_time, 
                                                                 end_time, 
                                                                 completed_chunks)
                if performance is not None:
                    return round(performance, 4) 

            return None
                                                            
        except Exception:
            BatchProcessManager.logger.error('Getting process unit[%s] performance failed:%s' % 
                                             (process_unit_name, traceback.format_exc()))
            raise
        
    def query_messages(self, process_unit_name, **filters):
        '''
        Queries on process unit messages.
        
        @param process_unit_name: process unit name
        @param **filters: 
            levels : a list including ERROR, INFO, WARNING
            from_date : from date
            to_date : to date
            contains : text, %text, text%, %text%
            limit: limit of messages that should be return.
            from_serial: serial of message 
            
        @return: [DynamicObject<message_time, name, level, message>]
        '''
        
        process_unit = self.get_process_unit(process_unit_name)
        return process_unit.get_message_stream().query(**filters)
    
    def get_last_error(self, process_unit_name):
        '''
        Returns last error which is written.
        
        @param process_unit_name: process unit name
        @return: str
        '''
        
        process_unit = self.get_process_unit(process_unit_name)
        return process_unit.get_message_stream().get_last_error()
    
    def truncate_messages(self, process_unit_name):
        '''
        Truncates message stream.

        @param process_unit_name: process unit name
        '''
        
        process_unit = self.get_process_unit(process_unit_name)
        return process_unit.get_message_stream().truncate()
    
    def get_joined_groups(self, process_unit_name):
        '''
        Returns the groups which the process unit should be waited for.
        
        @param process_unit_name: process unit name
        @return: []
        '''
        
        process_unit = self.get_process_unit(process_unit_name)
        return process_unit.get_joined_groups()
        
    def get_joined_units(self, process_unit_name):
        '''
        Returns the units which the process unit should be waited for.
        
        @param process_unit_name: process unit name
        @return: []
        '''
        
        process_unit = self.get_process_unit(process_unit_name)
        return process_unit.get_joined_units()
        
    def get_default_settings(self, process_unit_name):
        '''
        Returns default settings of given process unit.
        
        @param process_unit_name: process unit name
        @return: DynamicObject
        '''
        
        # Getting process unit default parameters
        params = self.__get_process_unit_config__(process_unit_name)
        
        return DynamicObject(params)


class ProcessUnitInformation(DynamicObject):
    '''
    
    '''
    def __init__(self, process_unit, parallel_executor=None):
        self.name = process_unit.get_name()
        self.group = process_unit.get_group_name()
        self.performance = None
        self.performance_unit = process_unit.get_performance_unit()
        self.info_count = process_unit.get_message_stream().get_info_count()
        self.error_count = process_unit.get_message_stream().get_error_count()
        self.warning_count = process_unit.get_message_stream().get_warning_count()
        self.parameters = {}#process_unit.get_params()
        
        self.start_time = None
        self.end_time = None
        self.preprocess_start_time = None 
        self.preprocess_end_time = None
        self.postprocess_start_time = None 
        self.postprocess_end_time = None
        self.completed_chunks = None
        self.running_chunks = None
        self.remained_chunks = None
        self.status = ParallelExecutor.StatusEnum.NOT_READY
        self.joined_groups = process_unit.get_joined_groups()
        self.joined_units = process_unit.get_joined_units()
        self.duration = None
        self.preprocess_duration = None
        self.postprocess_duration = None
        
        if parallel_executor is not None:
            self._populate_parallel_executor_info(process_unit, parallel_executor)
    
    def _get_process_unit_performance(self, process_unit, parallel_executor):
        '''
        Returns particular process unit information.
        
        @param process_unit:
        @param parallel_executor:
        '''
        try:
            if parallel_executor is not None:
                #raise Exception('Parallel executor does not exists for process unit [%s]'% process_unit.get_name())
                start_time, end_time = parallel_executor.get_running_times()
                completed_chunks = parallel_executor.get_compeleted_count()
                
                performance = process_unit.calculate_performance(start_time, 
                                                                 end_time, 
                                                                 completed_chunks)
                if performance is not None:
                    return round(performance, 4) 
            
            return None
        
        except Exception:
            BatchProcessManager.logger.error('Getting process unit[%s] performance failed:%s' % 
                                             (process_unit.get_name(), traceback.format_exc()))
            raise
    
    def _get_duration(self, start_time, end_time):
        duration = 0
        if start_time is not None \
            and end_time is not None:
            if end_time > 0:
                duration = end_time - start_time
        return duration
    
    def _populate_parallel_executor_info(self, process_unit, parallel_executor): 
        '''
        Populates the information of the parallel executor into the info object.
        
        @param parallel_executor: Parallel executor to get it's info
        '''
        self.performance = self._get_process_unit_performance(process_unit, parallel_executor)
        (self.start_time, 
         self.end_time) = parallel_executor.get_running_times()
        
        self.duration = self._get_duration(self.start_time, 
                                           self.end_time)
        self.start_time = time.ctime(self.start_time)
        if self.end_time is not None and self.end_time != 0:
            self.end_time = time.ctime(self.end_time)
        
        (self.preprocess_start_time, 
         self.preprocess_end_time) = parallel_executor.get_preprocess_times()
         
        self.preprocess_duration = self._get_duration(self.preprocess_start_time, 
                                                      self.preprocess_end_time)
        
        self.preprocess_start_time = time.ctime(self.preprocess_start_time)
        if self.preprocess_end_time is not None and self.preprocess_end_time != 0: 
            self.preprocess_end_time = time.ctime(self.preprocess_end_time) 
        
        (self.postprocess_start_time, 
         self.postprocess_end_time) = parallel_executor.get_postprocess_times()
         
        self.postprocess_duration = self._get_duration(self.postprocess_start_time, 
                                                       self.postprocess_end_time)
        
        if self.postprocess_start_time is not None and self.postprocess_start_time != 0:
            self.postprocess_start_time = time.ctime(float(self.postprocess_start_time))
        if self.postprocess_end_time is not None and self.postprocess_end_time != 0: 
            self.postprocess_end_time = time.ctime(float(self.postprocess_end_time)) 
        
        self.completed_chunks = parallel_executor.get_compeleted_count()
        self.running_chunks = parallel_executor.get_running_count()
        self.remained_chunks = parallel_executor.get_remained_count()
        self.status = parallel_executor.get_status()
        self.thread_count = parallel_executor.get_size()