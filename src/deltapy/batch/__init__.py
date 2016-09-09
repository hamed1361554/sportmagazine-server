'''
Created on Nov 5, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

class BatchPackage(Package):
    '''
    Batch processing package.
    '''
    
    __depends__ = ['deltapy.config', 
                   'deltapy.logging', 
                   'deltapy.commander']
    