'''
Created on Feb 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

MULTI_THREAD_PROCESS_REQUEST_PROCESSOR = 'deltapy.request_processor.multi_threaded'

class MultiThreadedRequestPrcessorPackage(Package):
    '''
    Request processor package class
    '''
    
    __depends__ = ['deltapy.commander', 
                   'deltapy.security',]