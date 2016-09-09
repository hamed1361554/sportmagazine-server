# DeltaConsole, A console for DeltaPy applications.
# Copyright (C) 2009-2011  Aidin Gharibnavaz <aidin@aidinhut.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on Nov 15, 2009
@author: Abi.Mohammadi & Majid.Vesal
'''

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
    '''Provides functionality for converting external types to
    internal types and vice versa
    '''
    
    def __init__(self):
        self.__internal_traverser = ObjectTraverser(self.internal_convert)
        self.__external_traverser = ObjectTraverser(self.external_convert)
    
    def internal_convert(self, obj):
        return obj
    
    def external_convert(self, obj):
        return obj

    def to_internal(self, obj):
        '''Converts an extranal object type to internal type.
        
        @param obj: external object
        @return: object
        '''
        return self.__internal_traverser.update(obj)
    
    def to_external(self, obj):
        '''Converts an internal object type to external object type.
        
        @param obj: internal object
        @return: object
        '''
        return self.__external_traverser.update(obj)
    