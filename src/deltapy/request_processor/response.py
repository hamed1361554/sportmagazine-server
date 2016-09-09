'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import datetime

from deltapy.core import DynamicObject

class Response(DynamicObject):
    def __init__(self, request, result, call_context):
        DynamicObject.__init__(self)
        self.request_id = request.id
        self.transaction_id = request.transaction_id
        self.trace_id = request.trace_id
        self.result = result
        self.context = call_context
        self.request_date = request.request_date
        self.recieve_date = request.recieve_date
        self.send_date = datetime.datetime.now()
