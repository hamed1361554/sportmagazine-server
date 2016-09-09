'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

class DatabasePackage(Package):
    '''
    Database package.
    '''
    
    __depends__ = ['deltapy.logging', 'deltapy.event_system']
