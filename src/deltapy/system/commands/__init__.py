'''
Created on Sep 2, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.commander.decorators import command
import deltapy.commander.services as commander
import deltapy.packaging.services as packaging
import deltapy.application.services as application

@command('package.load')
def load_package(package_name):
    """
    this function loads given package into the application.
    @param package_name: name of the package 
    """
    return packaging.load(package_name)

@command('package.unload')
def unload_package(package_name):
    """
    this function unloads given package from the application.
    @param package_name: name of the package 
    """
    return packaging.unload(package_name)

@command('package.reload')
def reload_package(package_name):
    """
    this function reloads given package into the application.
    @param package_name: name of the package 
    """
    return packaging.reload(package_name)

@command('package.list')
def list_packages(parent_name = None):
    """
    this function returns list of loaded packages of given parent.
    @param parent_name: name of the parent package, default is None. 
    """
    packages = packaging.get_loaded_packages(parent_name)
    results = []
    for pkg in packages:
        results.append(pkg.get_name())    
    return results

@command('package.doc')
def package_doc(package_name):
    """
    this function returns document of given package.
    @param package_name: name of the package. 
    """
    package = packaging.get_package(package_name)
    if package:
        return package.get_doc()
    return "package [%s] not found!"% package_name

@command('help')    
def show_help(scope, name):
    """
    this command shows the help of object using scope and name.
    @param scope: name of scope  eg. 'command', 'package' ...
    @param name: name or key of object.  
    """
    if scope == 'command':
        return command_doc(name)
    elif scope == 'package':
        return package_doc(name)
    return "scope [%s] not found!"%scope

