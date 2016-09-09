'''
Created on Jan 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import time
from deltapy.core import DeltaObject, DynamicObject

class BatchStream(DeltaObject):
    '''
    Provides a stream for writing batch processing information.
    '''
    
    class LevelEnum:
        ERROR = 'ERROR'
        INFO = 'INFO'
        WARNING = 'WARNING'
    
    def __init__(self, process_unit, size):
        DeltaObject.__init__(self)
        
        self.__process_unit = process_unit
        self.__last_error = None
        self.__size = size
        self.__error_count = 0
        self.__warning_count = 0
        self.__info_count = 0
        
    def get_size(self):
        '''
        Returns stream size.
        
        @return: int
        '''
        
        return self.__size
    
    def set_size(self, size):
        '''
        Sets stream buffer size.
        '''
        
        self.__size = size
        
    def get_process_unit(self):
        '''
        Returns batch stream's process unit instance.
        
        @return: ProcessUnit
        '''
        
        return self.__process_unit
    
    def _emit_(self, record):
        '''
        Emits changes to 
        
        @param record: emit record:
            message_time: message time
            name: name
            level: level
            message: message
        '''
        
        raise NotImplementedError()
    
    def get_error_count(self):
        '''
        Returns error records count.
        
        @return: int
        '''
        
        return self.__error_count
    
    def error(self, message):
        '''
        Writes with error tag.
        
        @param message: message
        '''

        self.write(BatchStream.LevelEnum.ERROR, message)
        self.__error_count += 1
        
    def get_info_count(self):
        '''
        Returns info records count.
        
        @return: int
        '''
        
        return self.__info_count
    
    def info(self, message):
        '''
        Writes with info tag.
        
        @param message: message
        '''

        self.__info_count += 1
        self.write(BatchStream.LevelEnum.INFO, message)
        
    def get_warning_count(self):
        '''
        Returns warning records count.
        
        @return: int
        '''
        
        return self.__warning_count
        
    def warning(self, message):
        '''
        Writes with warning tag.
        
        @param message: message
        '''

        self.__warning_count += 1
        self.write(BatchStream.LevelEnum.WARNING, message)
    
    def write(self, level, message):
        '''
        Writes message in batch stream.
        
        @param level: 
            ERROR,
            WARNING,
            INFO
        @param message: message
        '''
        
        emit_record = DynamicObject(time = time.time(),
                                    name = self.__process_unit.get_name(),
                                    level = level.upper(),
                                    message = message)
        
        if level == 0:
            self.__last_error = emit_record 
        
        self._emit_(emit_record)
        
    def query(self, **filters):
        '''
        Queries on message buffer with given filters.
        
        @param **filters: 
            level : ERROR, INFO, WARNING
            from_date : from date
            to_date : to date
            contains : text, %text, text%, %text% 
        '''
        
        raise NotImplementedError()
        
    def get_last_error(self):
        '''
        Returns last error which is written.
        
        @return: str
        '''
        
        return self.__last_error
    
    def truncate(self):
        '''
        Truncates stream.
        '''
        
        self.__error_count = 0
        self.__warning_count = 0
        self.__info_count = 0
        self.__last_error = None
