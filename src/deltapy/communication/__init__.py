'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

from deltapy.packaging.package import Package

class CommunicationPackage(Package):
    '''
    '''

    __depends__ = ['deltapy.config', 
                   'deltapy.logging', 
                   'deltapy.config', 
                   'deltapy.commander', 
                   'deltapy.event_system',
                   'deltapy.security',
                   'deltapy.request_processor']

