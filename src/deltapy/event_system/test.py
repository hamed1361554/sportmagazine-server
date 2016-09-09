'''
Created on Apr 9, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.event_system.manager import DeltaEventManager
from deltapy.event_system.event import DeltaEvent
from deltapy.event_system.event_handler import DeltaEventHandler
from deltapy.event_system.decorators import before_handler,\
    after_handler, delta_event


@delta_event('ADD_EVENT')
def add(a,b):
    return a+b

@before_handler('ADD_EVENT', 'BEFORE_ADD')
def before(params):
    print "before execute:",params
    
@after_handler('ADD_EVENT', 'AFTER_ADD')
def after(params):
    print "after execute:",params
                

#r = e.fire(2,3)

r = add(2,3)
print ">>>", r
