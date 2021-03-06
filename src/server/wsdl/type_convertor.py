"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

import copy

class ObjectTraverser(object):
    def __init__(self, traverse_func):
        self.__traverse_func = traverse_func
        
    def __traverse__(self, obj):
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
        return self.__traverse_func(obj)
        
    def update(self, obj):
        return self.__traverse__(obj)
    
    def clone(self, obj):
        clone_obj = copy.deepcopy(obj)
        return self.update(clone_obj)


class TypeConvertor(object):
    '''
    Provides functionality for converting external types to
    internal types and vice versa
    '''
    
    def __init__(self):
        """

        """

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
