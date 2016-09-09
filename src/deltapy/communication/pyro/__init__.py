'''
Created on Sep 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package
import deltapy.communication.services as communication
from deltapy.communication.pyro.factory import PyroFactory   

class PyroPackage(Package):
    def load(self):
        Package.load(self)
        
        communication.register_factory('pyro', PyroFactory())
    
    def unload(self):
        Package.unload(self)