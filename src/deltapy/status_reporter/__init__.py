'''
Created on Nov, 2013

@author: Nastaran & Aidin
'''

from deltapy.packaging.package import Package

class StatusReporterPackage(Package):
    '''
    '''

    __disable__ = True
    __depends__ = ['deltapy.event_system',
                   'deltapy.logging',
                   'deltapy.security']