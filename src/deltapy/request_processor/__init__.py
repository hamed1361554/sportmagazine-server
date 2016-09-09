'''
Created on Feb 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

APP_REQUEST_PROCESSOR = 'deltapy.request_processor'

class RequestPrcessorPackage(Package):
    '''
    Request processor package class
    '''
    
    __depends__ = ['deltapy.commander', 
                   'deltapy.security',
                   'deltapy.event_system']
