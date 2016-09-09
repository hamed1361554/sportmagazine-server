'''
Created on Aug 14, 2009

@author: abi.mohammadi, majid.vesal
'''

import sys
import os
import ConfigParser

from deltapy.core import DeltaException, DeltaObject
from deltapy.packaging.package import Package, PackageException
from deltapy.utils import get_module_dir, get_module_parent
import deltapy.application.services as application_services

class PackageManagerException(DeltaException):
    pass
       
class DependencyException(PackageManagerException):
    '''
    A class for handling packages dependency exceptions.
    '''
    pass

class PackageManager(DeltaObject):
    '''
    Provides some functionality for managing packages. 
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        self.__loaded_packages__ = {}
        self.__hooks = []
        self.__disabled_packages = []
        self._read_disabled_packages_config_()
        
    def _read_disabled_packages_config_(self):
        '''
        '''
        
        try:
            setting_folder = \
                application_services.get_default_settings_folder_name()
            package_dir = \
                get_module_dir(application_services.get_name())
            settings_dir = \
                os.path.join(package_dir, setting_folder)
                
            app_setting_file_name = \
                os.path.join(settings_dir, 'app.config')    
            
            config_parser = ConfigParser.ConfigParser()
            config_parser.read(app_setting_file_name)
            
            if config_parser.has_section('packages'):
                disabled_packages = config_parser.get('packages', 
                                                      'disabled_packages', 
                                                      None)
                if disabled_packages is not None:
                    disabled_packages_list = disabled_packages.split(',')
                    for disabled_package in disabled_packages_list:
                        striped_disabled_package = disabled_package.strip() 
                        if striped_disabled_package != '':
                            self.__disabled_packages.append(striped_disabled_package)
        except:
            import traceback
            print traceback.format_exc()
                
    def __reset_package__(self, package_name):
        related_modules = self.get_related_modules(package_name)
        for module in related_modules:
            if module.find(package_name) == 0:
                sys.modules.pop(module)
        
    def get_related_modules(self, package_name):
        '''
        Returns related modules of the package.
        
        @param package_name: package name
        '''
        
        return [module for module in sys.modules if module.find(package_name) == 0]
    
    def probe_package_class(self, parent, package_name, package_class):
        '''
        Probes the package class.
        
        @param parent: parent
        @param package_name: package name
        @param package_class: package class
        @return: boolean
        '''
        for hook in self.__hooks:
            if not hook.probe_package_class(self,
                                            parent,
                                            package_name, 
                                            package_class):
                return False
        return True
    
    def before_load(self, parent, package_name):
        '''
        Is called before loading package.
        
        @param parent: parent
        @param package_name: package name
        '''
        for hook in self.__hooks:
            hook.before_load(self,
                             parent,
                             package_name)        

    def after_load(self, 
                   parent, 
                   package_name, 
                   package):
        '''
        Is called after loading package.
        
        @param parent: parent
        @param package_name: package name
        @param package: package instance
        '''
        for hook in self.__hooks:
            hook.after_load(self,
                            parent,
                            package_name,
                            package)        

    def before_unload(self, package_name):
        '''
        Is called before loading package.
        
        @param parent: parent
        @param package_name: package name
        '''
        for hook in self.__hooks:
            hook.before_load(self,
                             package_name)        

    def after_unload(self, package_name):
        '''
        Is called after loading package.
        
        @param parent: parent
        @param package_name: package name
        @param package: package instance
        '''
        for hook in self.__hooks:
            hook.after_unload(self,
                            package_name)        

    def __get_package_class__(self, parent, package_name):
        if package_name not in self.__loaded_packages__:
            try:
                module = __import__(package_name, fromlist=parent or [])
            except ImportError:
                return None, None
                
            package_class = None
            for cls in module.__dict__.values():
                try:
                    if cls is not Package and issubclass(cls, Package):
                        if not getattr(cls, '__disable__') and package_name not in self.__disabled_packages:
                            package_class = cls
                            break
                        else:
                            print "Package [%s] is disable." % package_name 
                except TypeError:
                    pass
            return module, package_class
        
        return None, None
    
    def __auto_import__(self, package_name, parent):
        try:
            package_dir = get_module_dir(package_name)
            sub_modules = os.listdir(package_dir)
            for module_name in sub_modules:
                if module_name.find('__init__.py') == 0:
                    continue
                head, sep, tail = module_name.partition('.')
                module = __import__("%s.%s" % (package_name, head), fromlist=parent or [])
        except Exception:
            print 'Error in loading package [{0}]'.format(package_name)
            raise 
    
    def __load__(self, package_name, parent = None):
        
        # Doing before loading package actions.
        self.before_load(parent, package_name)
        
        # Getting package class
        module, package_class = self.__get_package_class__(parent, package_name)
        
        if not package_class:                
            #self.__reset_package__(package_name)
            return None
        
        if self.probe_package_class(parent, 
                                    package_name, 
                                    package_class):
            
            # Checking dependencies
            self._load_depends_(package_class, parent)
            
            # Creating instance...
            package = package_class()
            package.module = module
            package.name = module.__name__
            
            # Loading package...
            package.load()
            
            # Getting auto import modules
            auto_imports = getattr(package_class, '__auto_imports__')
            
            # Registering package...
            self.__loaded_packages__[package_name] = package
    
            package_dir = os.path.dirname(module.__file__)
            sub_dirs = os.listdir(package_dir)
            auto_imports = list(set(sub_dirs).intersection(set(auto_imports)))
            sub_packages = auto_imports + \
                list(set(sub_dirs).difference(set(auto_imports)))
            for sub_package in sub_packages:
                if sub_package.find('.') < 0:
                    pkg = self.__load__("%s.%s" % (package_name, 
                                                   sub_package), 
                                        [package_name])
                    if sub_package in auto_imports:
                        self.__auto_import__("%s.%s" % (package_name, 
                                                        sub_package), 
                                             [package_name])
                        
                    if pkg:
                        package.add_package(pkg)
                    
            
            print "Package [%s] loaded." % package_name
            
            self.after_load(parent, package_name, package)
            
            return package
        
    def _load_depends_(self, package_class, parent):
        '''
        Loads all packages which this packages depends those.
        
        @param package_class: package class
        @param parent: parent
        '''
        for package_name in package_class.__depends__:
            package = self.__load__(package_name, parent)
            if not package:
                DependencyException('Loading package[%s] failed. Could not load package[%s]' % (package_class, package_name))
            
    def load(self, package_name):
        '''
        Loads the package and it's sub packages.
        
        @param package_name: package name
        '''
        
        print ">> Disabled packages:"
        for disabled_package in self.__disabled_packages:
            print "    [%s]" % disabled_package 
        
        parent = []
        if get_module_parent(package_name):
            parent.append(get_module_parent(package_name))  
        self.__load__(package_name, parent)
        path = get_module_dir(package_name)
        sub_packages = os.listdir(path)
        for sub_package in sub_packages:
            if sub_package.find('.') < 0:
                self.__load__("%s.%s" % (package_name, sub_package), [package_name])
        
        loaded_packages_count = len(self.get_loaded_packages(package_name))        
        
        print ""
        print ">> %s:[%d] packages loaded." % (package_name, loaded_packages_count)
        print ">> Total loaded packages: %d" % (len(self.get_loaded_packages()))
        print ">> Disabled packages: %d" % (len(self.__disabled_packages))
        print ""
        
        return loaded_packages_count
                
    def get_package(self, package_name):
        '''
        Returns the package by the given name.
        
        @param package_name: package name
        '''
        return self.__loaded_packages__.get(package_name, None)            
    
    def unload(self, package_name):
        '''
        Unloads the package completely.
        
        @param package_name: package name
        '''
        
        self.before_unload(package_name)
        
        package = self.get_package(package_name)
        if package:            
            if not package.__unloadable__:
                raise PackageException("Package [%s] is unloadable." % package_name)
            print "Unloading packages from[%s]" % package            
            try:
                import deltapy.commander.services as commander
                commander.remove_commands(package_name)
            except ImportError:
                pass
            
            for sub_package in package.get_packages():
                self.unload(sub_package)
        
            package.unload()
        
            self.__reset_package__(package_name)
            
            module = self.__loaded_packages__.pop(package_name)
            
            del module
            del package
            
            self.after_unload(package_name)
    
    def reload(self, package_name):
        '''
        Reloads the package.
        
        @param package_name: package name
        '''
        package = self.get_package(package_name)
        if package:
            package_name = package.module.__name__
            self.unload(package_name)
            self.load(package_name)
        
    def get_loaded_packages(self, parent_name = None):
        '''
        Returns all loaded package in parent package domain.
        
        @param parent_name: parent package name
        @return: list<Package>
        '''
        
        packages = self.__loaded_packages__.values()
        results = []
        if not parent_name:
            results = packages
        else:
            for pkg in packages:
                if hasattr(pkg,'module') \
                    and pkg.module.__name__.find(parent_name) == 0:
                    results.append(pkg)
        return results
    
    def get_disabled_packages(self):
        '''
        Returns all disabled packages.
        
        @return: list<Package>
        '''
        return self.__disabled_packages
    
    def add_hook(self, hook):
        '''
        Sets the package manager hook.
        
        @param hook: hook instance
        '''
        
        self.__hooks.append(hook)
        
    def get_hooks(self):
        '''
        Returns the package manager hook.
        
        @return: PackageManagerHook
        '''
        
        return self.__hooks
    
