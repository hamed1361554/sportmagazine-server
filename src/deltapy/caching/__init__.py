'''
Created on Aug 18, 2009

@author: mohammadi, vesal
'''

from deltapy.packaging.package import Package

class CachePackage(Package):
    '''
    Cache package.
    '''
    
    __depends__ = ['deltapy.logging']

    
        
        