'''
Created on Oct 22, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
import time
import datetime

class IScavenger:
    '''
    Cache scavenger interface.
    '''
    def scavenge(self, cache, cache_item):
        '''
        Scavenges the cache or cache item.
        @param cache: cache instance
        @param cache_item: cache item
        '''
        
    def initialize(self, cache):
        '''
        Initializes the scavenger.
        
        @param cache: cache instance
        '''
        
class LifeTimeScavenger(IScavenger):

    def __init__(self, **durations):
        '''
        Weeks,
        Days,
        Hours,
        Minutes,
        Seconds,
        '''
        
        weeks = durations.get('weeks', 0)
        days = durations.get('days', 0)
        hours = durations.get('hours', 0)
        minutes = durations.get('minutes', 0)
        seconds = durations.get('seconds', 0)
        
        days += weeks * 7
        hours += days * 24
        minutes += hours * 60
        seconds += minutes * 60
        
        self._lifetime = seconds         
    
    def scavenge(self, cache, cache_item):
        if self._lifetime > 0 and time.time() > (cache.get_last_reset_time() + self._lifetime):
            cache.reset()            

class AbsoluteTimeScavenger(IScavenger):

    def __init__(self, **durations):
        '''
        Month,
        Day,
        Hour,
        Minute,
        Second,
        '''
        
        self.month = durations.get('month', -1)
        self.day = durations.get('day', -1)
        self.hour = durations.get('hour', -1)
        self.minute = durations.get('minute', -1)
        self.second = durations.get('second', 0)
        
    
    def scavenge(self, cache, cache_item):
        now = datetime.datetime.now()
        
        month = self.month
        if self.month < 0 :
            month = now.month
        
        day = self.day
        if self.day < 0 :
            day = now.day
        
        hour = self.hour
        if self.hour < 0 :
            hour = now.hour

        minute = self.minute    
        if self.minute < 0 :
            minute = now.minute
        
        second = self.second
        if self.second < 0 :
            second = now.second 

        if month == now.month and \
            day == now.day and \
            hour == now.hour and \
            minute == now.minute and \
            second == now.second :
            
            if time.time() - cache.get_last_reset_time() >= 1.0:
                cache.reset()