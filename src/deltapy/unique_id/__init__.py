'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

UNIQUE_ID_MANAGER = 'deltapy.unique_id_manager'

class UniqueIDManagerPackage(Package):
    '''
    '''
    
    __depends__ = ['deltapy.commander']
    
