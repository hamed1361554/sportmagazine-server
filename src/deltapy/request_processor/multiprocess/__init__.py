'''
Created on Feb 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

MULTI_PROCESS_REQUEST_PROCESSOR = 'deltapy.request_processor.multi_process'

class MultiProcessRequestPrcessorPackage(Package):
    '''
    Multiple process request processor package class
    '''
    
    __depends__ = ['deltapy.commander', 
                   'deltapy.security']