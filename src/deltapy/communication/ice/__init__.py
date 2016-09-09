'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.utils import get_module_dir
import Ice
import os
Ice.loadSlice(os.path.join(get_module_dir('deltapy.communication.ice'), 'services.ice'))
import DeltaIce
from deltapy.packaging.package import Package
import deltapy.communication.services as communication
  

class IcePackage(Package):

    __disable__ = True

    def load(self):
        Package.load(self)
        
        from deltapy.communication.ice.factory import IceFactory 
        communication.register_factory('ice', IceFactory())
    
    def unload(self):
        Package.unload(self)
      
