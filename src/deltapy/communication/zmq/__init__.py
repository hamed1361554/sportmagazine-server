'''
Created on Sep 16, 2014

@author: Abi.Mohammadi
'''

from deltapy.packaging.package import Package
from deltapy.communication.zmq.factory import ZmqFactory

import deltapy.communication.services as communication


class ZmqPackage(Package):
    '''
    Zmq package
    '''

    __disable__ = True

    def load(self):
        '''
        Loads package.
        '''
        
        Package.load(self)
        
        # Registering pyro4 factory
        communication.register_factory('zmq', ZmqFactory())

    def unload(self):
        '''
        Unloads package.
        '''
        Package.unload(self)
