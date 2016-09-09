'''
Created on Oct 26, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject

class PackageManagerHook(DeltaObject):
    '''
    Package manager hook.
    '''
    
    def probe_package_class(self, manager, parent, package_name, package_class):
        '''
        Probes the package class.
        
        @param manager: package manager
        @param parent: parent
        @param package_name: package name
        @param package_class: package class
        @return: boolean
        '''
        return True
    
    def before_load(self, manager, parent, package_name):
        '''
        Is called before loading package.
        
        @param manager: package manager
        @param parent: parent
        @param package_name: package name
        '''
        pass

    def after_load(self, manager, parent, package_name, package):
        '''
        Is called after loading package.
        
        @param manager: package manager
        @param parent: parent
        @param package_name: package name
        @param package: package instance
        '''
        pass
    
    def before_unload(self, manager, package_name):
        '''
        Is called after loading package.

        @param manager: package manager
        @param package_name: package name
        '''
        pass

    def after_unload(self, manager, package_name):
        '''
        Is called after loading package.
        
        @param manager: package manager
        @param package_name: package name
        '''
        pass