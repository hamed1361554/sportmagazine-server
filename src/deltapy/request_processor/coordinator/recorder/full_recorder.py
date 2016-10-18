'''
Created on May 25, 2015

@author: Hamed
'''

import datetime

from deltapy.core import DynamicObject
from deltapy.request_processor.coordinator.recorder.simple_recorder import SimpleRecorder


class FullRecorder(SimpleRecorder):
    '''
    Full Recorder
    '''

    def __init__(self):
        '''
        Initializes simple recorder.
        '''

        SimpleRecorder.__init__(self)

        self._set_name_('full_recorder')

    def _fill_request_data(self, request, **options):
        '''
        Fills request data based on given parameters.
        '''

        super(FullRecorder, self)._fill_request_data(request, **options)

        client_response = options.get('client_response')
        if client_response is not None:
            response_data = \
                DynamicObject(send_date=datetime.datetime.now(),
                              command_result=client_response)
            request.data.response_data = response_data

        client_request = options.get('client_request')
        if client_request is not None:
            request.data.call_context = client_request.context

    def set_completed(self, request, **options):
        '''
        Completes the state of the given request.

        @param str request_id: request ID
        @param request_id: request ID
        '''

        self._fill_request_data(request,
                                client_request=options.get('client_request'),
                                client_response=options.get('client_response'))
        return request
