'''
Created on Feb 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

COMPLEX_MULTI_PROCESS_REQUEST_PROCESSOR = 'deltapy.request_processor.complex_multi_process'

class ComplexMultiProcessRequestPrcessorPackage(Package):
    '''
    Multiple threaded process request processor package class
    '''
    
    __depends__ = ['deltapy.commander', 
                   'deltapy.security']
