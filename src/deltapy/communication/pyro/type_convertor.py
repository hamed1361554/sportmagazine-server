'''
Created on Nov 24, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
from decimal import Decimal

from deltapy.communication.type_convertor import TypeConvertor
from deltapy.core import DynamicObject
import deltapy.config.services as config_services
from deltapy.communication.pyro import utils
import cPickle

class PyroTypeConvertor(TypeConvertor):
    '''
    Pyro type convertor.
    '''
    
    def __init__(self):
        TypeConvertor.__init__(self)
        self._str_converter = utils.StringConverter()

    def external_convert(self, obj):
        if isinstance(obj, DynamicObject):
            return dict(obj)
        elif isinstance(obj, buffer):
            return str(obj)
        elif isinstance(obj, str):
            return self._str_converter.to_external(obj)
        return obj

    def internal_convert(self, obj):
        if isinstance(obj, dict):
            return DynamicObject(obj)
        if isinstance(obj, (str, unicode)):
            return self._str_converter.to_internal(obj)
        return obj
    
    def to_external(self, obj):
        '''
        Converts an internal object type to external object type.
        
        @param obj: internal object
        @return: object
        '''
        
        exobj = cPickle.loads(cPickle.dumps(obj))

        return TypeConvertor.to_external(self, exobj)