# -*- coding: cp1256 -*-
'''
Created on Nov 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import re
import copy

from deltapy.logging.services import get_logger
from deltapy.core import DeltaObject, DeltaException
from deltapy.security.session.services import get_current_user


class TypeConverterException(DeltaException):
    '''
    Is raised when type converter encounters error.
    '''


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

    LOGGER = get_logger(name='root')
    
    def __init__(self):
        '''
        Initializes type converter.
        '''

        NullTypeConvertor.__init__(self)
        
        self.__internal_traverser = ObjectTraverser(self.safe_internal_convert)
        self.__external_traverser = ObjectTraverser(self.safe_external_convert)

        self._invalid_phrases = \
            ['`', '^', '\\', 'script', 'html', 'xhtml', 'colon', 'base64',
             'import', 'exec', 'eval', 'compile', 'getattr', 'setattr',
             '__getattr__', '__getattribute__', '__setattr__', '__delattr__',
             '__class__', '__module__', 'BANNED_WORDS']
        self._invalid_regex = \
            [r'[\s\S]*<[\s\S]*>[\s\S]*',
             r'[\s\S]*[&#"\'][\s\S]*;[\s\S]*',
             r'([\s\"\'`;\/0-9\=]+on\w+\s*=)']
        self._combined_invalid_regex = \
            re.compile("(" + ")|(".join(self._invalid_regex) + ")")

    def _normalize(self, obj):
        return obj.lower().strip().replace('\n', '').replace('\r', '')

    def _validate(self, obj):
        if not isinstance(obj, (str, unicode)):
            return

        normalized_obj = self._normalize(obj)

        for invalid_phrase in self._invalid_phrases:
            if invalid_phrase in normalized_obj:
                raise TypeConverterException(_('Invalid phrase [{0}] got detected.'.format(invalid_phrase)))

        if re.match(self._combined_invalid_regex, normalized_obj):
            raise TypeConverterException(_('Invalid phrase [{0}] got detected.'.format(obj)))

    def safe_internal_convert(self, obj):
        #self._validate(obj)
        return self.internal_convert(obj)

    def safe_external_convert(self, obj):
        return self.external_convert(obj)
    
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
    
