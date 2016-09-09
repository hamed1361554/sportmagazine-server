'''
Created on Mar, 2015

@author: Aidin
'''

from deltapy.request_processor.request import RawRequest
from deltapy.communication.pyro.type_convertor import PyroTypeConvertor

CONVERTER = PyroTypeConvertor()

class PyroRawRequest(RawRequest):

    def get_converter(self):
        '''
        Gets a TypeConverter class, that should be called on the `request_dict',
        to convert Pyro types to the types RequestProcessor expected.
        '''

        return CONVERTER
