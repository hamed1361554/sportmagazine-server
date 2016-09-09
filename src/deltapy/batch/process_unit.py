'''
Created on Nov 6, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject
from deltapy.batch.memory_stream import BatchMemoryStream

class ProcessUnit(DeltaObject):
    '''
    Provides base functionality of a processor. 
    '''
    
    __joined_groups__ = []
    __joined_units__ = []
    
    def __init__(self,
                 name, 
                 group_name):
        DeltaObject.__init__(self)        
        self._set_name_(name)
        self.__group_name = group_name
        self.__params = None
        self._stream = BatchMemoryStream(self) 
        
    def get_group_name(self):
        '''
        Returns process unit group name.
        
        @return: str
        '''
        return self.__group_name
    
    def get_description(self):
        '''
        Returns process unit's description
        '''
        
        return self.__doc__
    
    def get_message_stream(self):
        '''
        Returns message stream.
        
        @return: BatchStream
        '''
        
        return self._stream
            
    def configure(self, **kwargs):
        '''
        Prepares processor for running task.
        '''
        self.__params = kwargs
        buffer_size = self.__params.get('buffer_size', 8096)
        self._stream.set_size(buffer_size)
        
    def get_params(self):
        '''
        Returns configuration params
        
        @return: {}
        '''
        return self.__params
    
    def create_chunks(self):
        '''
        Creates chunks and returns chunks.
        '''

        raise NotImplementedError()
    
    def process(self, chunk):
        '''
        Process method which overrides by the child class.
        
        @param chunk: chunk information
        '''

        raise NotImplementedError()
    
    def done(self):
        '''
        Finishes the processes which overrides by the child class.
        '''
        
        pass
    
    def failed(self, error):
        '''
        It will be called when an exception occurred.
        @param error: error object
        '''
        pass
    
    def stopping(self):
        '''
        Should be called when unit is going to stop.
        '''
        pass
    
    def get_performance_unit(self):
        '''
        Returns performance unit. For example TPS
        
        @return: str
        '''
    
        return 'Not determinated'
    
    def calculate_performance(self, start_time, end_time, compeleted_chunk):
        '''
        Calculates performance value.
        
        @return: float
        '''
               
        elapsed_time = (end_time - start_time) / 60.0

        if elapsed_time <= 0:
            return 0.0

        return float(compeleted_chunk) / elapsed_time
    
    def get_information(self):
        '''
        Returns process unit runtime information.
        
        @return: {}
        '''
        
        return {}
        
    def get_joined_groups(self):
        '''
        Returns the groups which the process unit should be waited for.
        
        @return: []
        '''
        
        params = self.get_params()

        # Getting joining information
        results = []
        if params is not None:
            joined_groups = params.get('joined_groups')
            if joined_groups is not None:
                results = list(eval(joined_groups))
            
        return list(set(self.__class__.__joined_groups__).union(set(results)))
        
    def get_joined_units(self):
        '''
        Returns the units which the process unit should be waited for.
        
        @return: []
        '''
        
        params = self.get_params()

        # Getting joining information
        results = []
        if params is not None:
            joined_units = params.get('joined_units')
            if joined_units is not None:
                results = list(eval(joined_units))
        
        return list(set(self.__class__.__joined_units__).union(set(results)))
                
