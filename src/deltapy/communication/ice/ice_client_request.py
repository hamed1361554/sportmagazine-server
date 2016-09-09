'''
Created on Mar 10, 2015

@author: Aidin
'''

from deltapy.request_processor.request import RawRequest
from deltapy.communication.ice.type_convertor import IceTypeConvertor

CONVERTER = IceTypeConvertor()

class IceRawRequest(RawRequest):

    def get_converter(self):
        '''
        Gets a TypeConverter class, that should be called on the `request_dict',
        to convert ICE types to the types RequestProcessor expected.
        '''

        return CONVERTER
