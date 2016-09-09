'''
Created on Aug 30, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

class CommanderPackage(Package):
    """
    this package manages all commands in the system.
    """
    
    __depends__ = ['deltapy.logging', 
                   'deltapy.transaction']
    __unloadable__ = False
    
    def load(self):
        Package.load(self)
        
        from deltapy.commander.components import TransactionalCommandManagerComponet
        from deltapy.application.services import register_component
        from deltapy.locals import APP_COMMANDER

        register_component(APP_COMMANDER, 
                           TransactionalCommandManagerComponet())
        
        
        
