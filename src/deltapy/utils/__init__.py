'''
Created on Aug 9, 2009

@summary: global utility functions. 
@author: abi m.s, majid v.a
'''

import threading
import os
import sys

#try:
#    import c_storm_aux as storm_aux
#    sys.modules['deltapy.utils.storm_aux'] = storm_aux
#except:
#    import _storm_aux as storm_aux
#    sys.modules['deltapy.utils.storm_aux'] = storm_aux

__object_path_cache_lock__ = threading.Lock()
__object_path_cache__ = {}

def get_object_path(obj_type):
    '''
    Returns class or function path. 
    
    @param obj_type: actualy it is the class type but it could be function
    '''
    
    if hasattr(obj_type, '__log_info__'):
        return obj_type.__log_info__
    module_name = str(obj_type.__module__)
    full_name = module_name + '.' + obj_type.__name__
    if __object_path_cache__.has_key(full_name):
        return full_name, __object_path_cache__[full_name]
    modules = [module_name]
    head = module_name
    while head.find('.') > 0:
        head, sep, tail = head.rpartition('.')
        modules.append(head)
        del sep, tail
    try:
        __object_path_cache_lock__.acquire()
        __object_path_cache__[full_name] = modules
        obj_type.__log_info__ = full_name, modules 
        return full_name, modules
    finally:
        __object_path_cache_lock__.release()
        
def get_module_parent(module_name):
    '''
    Returns the module directory.
    
    @param module: module object.
    @return: str of module dire
    '''
    
    parent = None
    
    if module_name.find('.') >= 0:
        parent, sep, tail = module_name.rpartition('.')
        del sep, tail        
    return parent

def get_module_dir(module_name):
    '''
    Returns the module directory.
    
    @param module: module object.
    @return: str of module dire
    '''
    
    module = sys.modules[module_name]
    
    return os.path.dirname(module.__file__)

def get_package_of(module_name):
    '''
    Returns the module package.
    
    @param module_name: module name
    @return: str
    '''

    if module_name.find('.') > 0:
        parent, sep, tail = module_name.rpartition('.')
        del sep, tail
        return parent
    return module_name

def write_log(filename, message, **options):
    '''
    
    @param filename:
    @param message:
    '''
    
    mode = options.get('mode', 'a')
    file = open(filename, mode)
    file.write('{message}\n'.format(message= message))
    file.close()