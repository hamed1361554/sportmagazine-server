'''
Created on Sep 5, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
import time

class TimeCounter:
    def __init__(self):
        self.counters = {}

    def start(self, name):
        if not self.counters.has_key(name):
            self.counters[name] = (time.time(), 0)

    def reset(self, name):
        self.counters[name] = (time.time(), 0)

    def stop(self, name):
        if name in self.counters:
            start, stop = self.counters.get(name)
            if stop == 0:
                self.counters[name] = (start, time.time())

    def get(self, name):
        return self.counters.get(name, (0, 0))
        
    def elapsed(self, name):
        if name in self.counters:
            start, stop = self.counters.get(name)
            if stop > 0:
                return stop - start
            return time.time() - start