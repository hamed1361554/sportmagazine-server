'''
Created on Sep 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package
import deltapy.communication.services as communication
from deltapy.communication.pymp.factory import PympFactory  

class PympPackage(Package):
    def load(self):
        Package.load(self)
        
        communication.register_factory('pymp', PympFactory())
    
    def unload(self):
        Package.unload(self)
