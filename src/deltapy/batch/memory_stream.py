'''
Created on Jan 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.batch.batch_stream import BatchStream

class BatchMemoryStream(BatchStream):
    '''
    Provides a memory stream.
    '''
    
    def __init__(self, process_unit, size = 1000):
        BatchStream.__init__(self, process_unit, size)
        
        self.__memory = []
        
    def _emit_(self, record):
        '''
        Emits changes to 
        
        @param record: emit record:
            emit_time: emit time
            name: name
            level: level
            message: message
        '''
        
        record.serial = 1 + len(self.__memory)
        self.__memory.append(record)
        if len(self.__memory) > self.get_size():
            self.__memory.pop(0)
            
    def truncate(self):
        '''
        Truncates the memory stream.
        '''
        
        BatchStream.truncate(self)
        
        self.__memory = []
        
    def query(self, **filters):
        '''
        Queries on message buffer with given filters.
        
        @param **filters: 
            levels : a list including ERROR, INFO, WARNING
            from_date : from date
            to_date : to date
            contains : text, %text, text%, %text%
            limit: limit of messages that should be return.
            from_serial: message serial 
        @return: [DynamicObject<message_time, name, level, message>]
        '''
        
        level_filters = filters.get('levels', ['ERROR','INFO', 'WARNING'])
        limit = filters.get('limit', -1)
        from_serial = filters.get('from_serial', 0)
        levels = []
        for level in level_filters:
            levels.append(level.upper())            
        from_date = filters.get('from_date', None)
        to_date = filters.get('to_date', None)
        contains = filters.get('contains', None)
        text = None
        start_text = None
        end_text = None
        exact_text = None
        
        if contains:
            if contains.startswith('%'):
                start_text = contains[1:]
            if contains.endswith('%'):
                end_text = contains[:len(contains) - 1]
            if start_text and end_text:
                text = contains[1:len(contains) - 1]
            if not start_text and not end_text and not text:
                exact_text = contains
            
        results = []
        for record in self.__memory:
            if record.level not in levels:
                continue
            
            if record.serial < from_serial:
                continue
                
            if from_date:
                if record.message_time < from_date:
                    continue
            if to_date:
                if record.message_time > to_date:
                    continue
            if text:
                if record.message.find(text) < 0:
                    continue
            elif start_text:
                if not record.message.startswith(start_text):
                    continue
            elif end_text:
                if not record.message.endswith(end_text):
                    continue
            elif exact_text:
                if record.message != exact_text:
                    continue                
            results.append(record)
        
        limited_results = results.reverse()
        if limit >= 0:
            limited_results = results[:limit] 
            
        return limited_results
                
    
