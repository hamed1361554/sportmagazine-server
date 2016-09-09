'''
Created on Dec 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

class TransactionPackage(Package):
    
    __depends__ = ['deltapy.logging', 
                   'deltapy.database']
