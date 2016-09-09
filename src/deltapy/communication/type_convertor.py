'''
Created on Nov 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject
import copy

class ObjectTraverser:
    def __init__(self, traverse_func):
        self.__traverse_func = traverse_func
        self.__traversed_objects = {}
        
    def __traverse__(self, obj):
        object_id  = id(obj)
        traversed_object = self.__traversed_objects.get(object_id)
        if traversed_object:
            return traversed_object

        if isinstance(obj, (list, tuple)):
            collection = []
            for v in obj:
                collection.append(self.__traverse__(v))
            if isinstance(obj, tuple):
                return tuple(collection)
            return collection
        if isinstance(obj, dict):
            for k in obj:
                obj[k] = self.__traverse__(obj[k])
                
        traversed_object = self.__traverse_func(obj)
        self.__traversed_objects[object_id] = traversed_object
        return traversed_object
        
    def update(self, obj):
        self.__traversed_objects = {}
        return self.__traverse__(obj)
    
    def clone(self, obj):
        clone_obj = copy.deepcopy(obj)
        return self.update(clone_obj)
    
class NullTypeConvertor(DeltaObject):
    def to_internal(self, obj):
        '''
        Converts an extranal object type to internal type.
        
        @param obj: external object
        @return: object
        '''
        
        return obj
        
    def to_external(self, obj):
        '''
        Converts an internal object type to external object type.
        
        @param obj: internal object
        @return: object
        '''

        return obj

class TypeConvertor(NullTypeConvertor):
    '''
    Provides functionality for converting external types to internal types and vice versa
    '''
    
    def __init__(self):
        NullTypeConvertor.__init__(self)
        
        self.__internal_traverser = ObjectTraverser(self.internal_convert)
        self.__external_traverser = ObjectTraverser(self.external_convert)
    
    def internal_convert(self, obj):
        return obj
    
    def external_convert(self, obj):
        return obj

    def to_internal(self, obj):
        '''
        Converts an extranal object type to internal type.
        
        @param obj: external object
        @return: object
        '''
        
        return self.__internal_traverser.update(obj)
    
    def to_external(self, obj):
        '''
        Converts an internal object type to external object type.
        
        @param obj: internal object
        @return: object
        '''

        return self.__external_traverser.update(obj)
    
