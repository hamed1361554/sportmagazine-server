'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

EVENT_MANAGER = 'deltapy.event_manager'

class EventSystemPackage(Package):
    '''
    Event system package.
    '''
    
    __depends__ = ['deltapy.logging']
