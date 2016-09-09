'''
Created on Sep 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package
import deltapy.communication.services as communication

class XmlrpcPackage(Package):
    def load(self):
        Package.load(self)
        
        from deltapy.communication.xmlrpc.factory import XmlrpcFactory   
        communication.register_factory('xmlrpc', XmlrpcFactory())
    
    def unload(self):
        Package.unload(self)