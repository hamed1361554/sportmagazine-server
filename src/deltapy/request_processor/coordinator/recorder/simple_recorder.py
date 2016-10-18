'''
Created on May 25, 2015

@author: Hamed
'''

from deltapy.core import DeltaObject, DeltaException


class SimpleRecorderRequestManagerException(DeltaException):
    '''
    Is raised when simple recorder request encounters an error.
    '''


class SimpleRecorder(DeltaObject):
    '''
    Simple Recorder
    '''

    def __init__(self):
        '''
        Initializes simple recorder.
        '''

        DeltaObject.__init__(self)

        self._set_name_('simple_recorder')

    def _fill_request_data(self, request, **options):
        '''
        Fills request data based on given parameters.
        '''

        client_request = options.get('client_request')
        if client_request is not None:
            request.data.command_args = client_request.command_args
            request.data.command_kwargs = client_request.command_kwargs

        request.data.error = options.get('error')

    def get(self, request, **options):
        '''
        Fetch request by given ID.

        @param dict request: request data
        '''

        return request

    def record(self, request, client_request, **options):
        '''
        Records a request data using the given information.

        @param str recorder_type: recorder type
        @param dict request: request data
        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str client_ip: client IP,
                            datetime receive_date: receive date,
                            datetime request_date: request date from client)
        '''

        return self._fill_request_data(request,
                                       client_request=client_request)

    def set_completed(self, request, **options):
        '''
        Completes the state of the given request.

        @param str request_id: request ID
        @param request_id: request ID
        '''

        self._fill_request_data(request,
                                client_request=options.get('client_request'))
        return request

    def set_failed(self, request, **options):
        '''
        Sets the state of the given request to failed.

        @param dict request: request
        '''

        self._fill_request_data(request,
                                client_request=options.get('client_request'),
                                error=options.get('error'))
        return request

    def get_request_state(self, request):
        '''
        Returns state of specified request.

        @param dict request: request

        @rtype: int
        @note:
            0: received
            1: completed
            2: failed
            3: reversed
        @return: request state
        '''

        return request.state