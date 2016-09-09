'''
Created on Mar, 2015

@author: Aidin
'''

from deltapy.request_processor.request import RawRequest
from deltapy.communication.zmq.type_convertor import ZmqTypeConvertor

CONVERTER = ZmqTypeConvertor()

class ZmqRawRequest(RawRequest):

    def get_converter(self):
        '''
        Gets a TypeConverter class, that should be called on the `request_dict',
        to convert JSON to the types RequestProcessor expected.
        '''

        return CONVERTER
