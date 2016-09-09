'''
Created on Aug 11, 2009

@author: mohammadi, vesal
'''

from deltapy.packaging.package import Package
 
class LoggingPackage(Package):
    '''
    Logging package.
    '''

    __depends__ = ['deltapy.config']
