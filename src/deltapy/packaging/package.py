'''
Created on Aug 9, 2009

@author: mohammadi, vesal
'''

from deltapy.core import DeltaObject
from deltapy.core import DeltaException

#import imp, sys
#import __builtin__
"""
def __delta_import__(name,globals={},locals={},fromlist=[], level = -1):
    '''
    
    @param name:
    @param globals:
    @param locals:
    @param fromlist:
    @param level:
    '''
    # check module name in sys cache 
    if name in sys.modules:
        return sys.modules[name]
    
    # finding module information
    file, path, description = imp.find_module(name)
    module = imp.load_module(name, file , path, description)
    
    # check if current module is delta package
    if hasattr(module,"__delta_module__"):
        __loaded_packages__[module.__name__] = module
    
    return module
"""

# replacing delta import function instead of built in import function.
#__builtin__.__import__ = __delta_import__

class PackageException(DeltaException):
    """
    ????
    """  
    pass

class Package(DeltaObject):
    """
    Every loadable packages must have a class in them that
    inhertited from this one.
    Nothing need to implement or override.

    Inherited class can set some special attributes:
    
        __depends__ : Can be set to a list of dependent packages.
                      (A list of strings)
        __auto_imports__ : 
        __unloadable__ : If sets to `True', the package cannot be
                         unloaded after its first load.
        __disable__ : If sets to `True', this package won't load.

    @note: There can be a `disabled_packages' option in the `packages'
           section of the `app.config', that defines which packages
           should be treated as disabled packages.
    """   
    
    __depends__ = []
    __auto_imports__ = ['components', 
                        'commands',
                        'event_handlers',
                        'permissions']
    __unloadable__ = True
    __disable__ = False
    
    def __init__(self):
        DeltaObject.__init__(self)
        self.__sub_packages__ = []
        self.__delta_module__ = True
        self.name = None
        self.module = None
        
    def get_packages(self):
        return self.__sub_packages__
    
    def add_package(self, package):
        self.__sub_packages__.append(package)
        
    def load_configs(self):
        if self.name:
            import deltapy.config.services as config
            config.load_all_configs(self.name)
            
    def load(self):
        try:
            self.load_configs()
        except:
            pass
    
    def unload(self):
        pass



    
