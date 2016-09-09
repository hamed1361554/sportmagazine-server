'''
Created on Aug 13, 2009

@author: majid v.a, abi m.s
'''

import datetime

from deltapy.core import DynamicObject
import deltapy.unique_id.services as unique_id_services


class RawRequest(object):
    '''
    Raw data of the request, that received from client.
    '''
    
    def __init__(self, request_dict):
        self._request_dict = request_dict
    
    def get_request_dict(self):
        '''
        Gets a ClientRequest object, based on raw request.
        '''

        return self._request_dict

    def get_converter(self):
        '''
        Gets a TypeConverter class, that should be called on the `request_dict',
        to convert it to the data types RequestProcessor expected.
        '''
        # By default, there's no converter.
        return None


class ClientRequest(DynamicObject):

    def __init__(self,
                 request_id, 
                 transaction_id,
                 trace_id,
                 request_date,
                 ip, 
                 ticket, 
                 user_name, 
                 command_key, 
                 command_args, 
                 command_kwargs,
                 timeout, 
                 context):

        DynamicObject.__init__(self)

        self.id = request_id
        if self.id is None:
            self.id = unique_id_services.get_id('uuid')
        self.trace_id = trace_id
        if self.trace_id is None:
            self.trace_id = unique_id_services.get_id('uuid')
        self.transaction_id = transaction_id
        if self.transaction_id is None:
            self.transaction_id = unique_id_services.get_id('uuid')
        self.ip = ip
        self.ticket = ticket
        self.user_name = user_name
        self.command_key = command_key
        self.command_args = command_args
        self.command_kwargs = command_kwargs
        self.context = context
        self.recieve_date = datetime.datetime.now()
        self.request_date = request_date
        self.timeout = timeout

    def __str__(self):
        result = _('id:[{0}], request date:[{1}], user:[{2}@{3}], command:[{4}]')
        return result.format(self.id, self.request_date, self.user_name, self.ip, self.command_key)
        
    @staticmethod
    def from_dict(request):
        return ClientRequest(request['id'],
                             request.get('transaction_id'),
                             request.get('trace_id'),
                             request['request_date'],
                             request['ip'],
                             request['ticket'],
                             request['user_name'],
                             request['command_key'],
                             request['command_args'],
                             request['command_kwargs'],
                             request.get('timeout'),
                             request['context'])
