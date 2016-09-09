'''
Created on Mar, 2015

@author: Aidin
'''

from deltapy.request_processor.request import RawRequest
from deltapy.communication.xmlrpc.type_convertor import XmlrpcTypeConvertor

CONVERTER = XmlrpcTypeConvertor()

class XmlrpcRawRequest(RawRequest):

    def get_converter(self):
        '''
        Gets a TypeConverter class, that should be called on the `request_dict',
        to convert Pyro types to the types RequestProcessor expected.
        '''

        return CONVERTER
