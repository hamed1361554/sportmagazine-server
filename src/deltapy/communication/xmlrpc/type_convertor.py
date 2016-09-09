'''
Created on Nov 24, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.type_convertor import TypeConvertor
from deltapy.core import DynamicObject
from decimal import Decimal

class XmlrpcTypeConvertor(TypeConvertor):
    '''
    Ice type convertor.
    '''
    
    def __init__(self):
        TypeConvertor.__init__(self)

    def external_convert(self, obj):
        #if isinstance(obj, str):
        #   return obj.decode('cp1256').encode('utf-8')
        if isinstance(obj, DynamicObject):
            return dict(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        return obj

    def internal_convert(self, obj):
        #if isinstance(obj, str):
        #   return obj.decode('utf-8').encode('cp1256')
        return obj
