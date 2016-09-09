'''
Created on Feb, 2015

@author: Aidin
'''

from deltapy.packaging.package import Package

SINGLE_PROCESS = 'deltapy.request_processor.single_process'

class SingleProcessPackage(Package):
    '''
    Provide SingleProcess request processor.
    '''

    __depends__ = ['deltapy.application',
                   'deltapy.configs',
                   'deltapy.request_processor']
