'''
Created on Jan 1, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.batch.process_unit import ProcessUnit
import deltapy.batch.services as batch_processor 
from deltapy.core import DeltaException

class CompositeProcessUnitException(DeltaException):
    '''    
    '''
    
class CompositeProcessUnit(ProcessUnit):
    '''
    Provides a process unit composition facility. 
    '''
    
    def __init__(self, 
                 name, 
                 group):
        ProcessUnit.__init__(self, name, group)
        self.__process_units = []
        self.__compeleted_sub_process_units = 0
        
    def add_process_unit(self, process_unit_name):
        '''
        Adds a process unit.
        @param process_unit_name: process unit name
        '''
        if process_unit_name not in self.__process_units: 
            self.__process_units.append(process_unit_name)
        
    def get_process_units(self):
        '''
        Returns list of added process units.
        '''
        return self.__process_units
    
    def create_chunks(self):
        '''
        Creates chunks and returns chunks.
        '''
        self.__compeleted_sub_process_units = 0
        return [1]

    def configure(self, **kwargs):
        '''
        Prepares processor for running task.
        '''
        
        process_units_str = kwargs.get('sequence', None)
        process_units = []
        if process_units_str != None:
            process_units = process_units_str.split(',') 
            
        for process_unit in process_units:
            self.add_process_unit(process_unit.strip())
        
        ProcessUnit.configure(self, **kwargs)
        
    def process(self, chunk):
        '''
        Process method which overrides by the child class.
        
        @param chunk: chunk information
        '''
        
        for process_unit in self.__process_units:
            params = {}
            params.update(self.get_params())
            #TODO: eval of sub configuration should be considered for sub units.
            params.update(self.get_params().get(process_unit, {}))
            batch_processor.start(process_unit, **params)
            batch_processor.join(process_unit)

            if not batch_processor.is_completed(process_unit):
                message = _('Process unit [{unit_name}] is [{status}].')
                raise CompositeProcessUnitException(message.format(unit_name = process_unit,
                                                                   status = batch_processor.get_status(process_unit)))
            self.__compeleted_sub_process_units +=1
            
    def stopping(self):        
        '''
        Should be called when unit is going to stop.
        '''
        for child_unit in self.__process_units:
            batch_processor.stop(child_unit)
    
    def calculate_performance(self, start_time, end_time, compeleted_chunk):
        '''
        Calculates performance value.
        
        @return: float
        '''
        
        return self.__compeleted_sub_process_units
