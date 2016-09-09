'''
Created on Oct 11, 2015

@author: Hamed
'''

from deltapy.packaging.package import Package
from deltapy.communication.thrift.factory import ThriftFactory
import deltapy.communication.services as communication
  

class ThriftPackage(Package):
    def load(self):
        Package.load(self)
        communication.register_factory('thrift', ThriftFactory())
    
    def unload(self):
        Package.unload(self)
