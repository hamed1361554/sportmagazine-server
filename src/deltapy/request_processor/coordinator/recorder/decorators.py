'''
Created on May 25, 2015

@author: Hamed
'''

import datetime

from deltapy.core import DeltaObject, DeltaException
from deltapy.request_processor.response import Response
from deltapy.request_processor.request import ClientRequest
from deltapy.security.session.services import get_current_session

import deltapy.transaction.services as transaction_services
import deltapy.request_processor.coordinator.services as coordinator_services


class RequestCoordinatorWrapperException(DeltaException):
    '''
    Is raised when request coordinator wrapper encounters error.
    '''


class RequestCoordinatorWrapper(DeltaObject):
    '''
    Request Coordinator Wrapper
    '''

    def __init__(self, key, **options):
        '''
        Initializes request coordinator decorator.

        @param key: recorder key
        @param recorder_type: recorder type
        '''

        DeltaObject.__init__(self)

        self._set_name_(key)
        self._recorder_type = options.get('recorder_type', 'full_recorder')
        self._should_be_reversed = options.get('should_be_reversed', True)

    def _create_request(self, *args, **kwargs):
        '''
        Creates request object.
        '''

        current_session = get_current_session()
        current_client_request = current_session.get_client_request()
        current_user_id = current_session.get_user_id()

        request = \
            ClientRequest.from_dict({'request_date': datetime.datetime.now(),
                                     'command_key': self.get_name(),
                                     'command_args': args[1:],
                                     'command_kwargs': kwargs,
                                     'id': current_client_request.id,
                                     'transaction_id': current_client_request.get('transaction_id'),
                                     'trace_id': current_client_request.get('trace_id'),
                                     'ip': current_session.get_client_ip(),
                                     'ticket': '',
                                     'user_name': '{0}-{1}'.format(current_user_id.branch_code,
                                                                   current_user_id.code),
                                     'context': current_session.get_call_context()})

        return request

    def _create_response(self, request, result):
        '''
        Creates response object.
        '''

        return Response(request, result, request.get('context'))

    def _attach_to_transaction(self, request):
        '''
        Attaches to current transaction to rollback request in case of error occurred.
        '''

        # Appending reverse callable for current transaction
        if self._should_be_reversed:
            current_transaction = transaction_services.get_current_transaction()
            current_transaction.add_before_rollback_trigger(self._reverse_request,request)

    def set_completed(self, result, *args, **kwargs):
        '''
        Is called when service executed correctly.
        '''

        request = self._create_request(*args, **kwargs)
        response = self._create_response(request, result)
        self._attach_to_transaction(request)
        coordinator_services.set_completed(self._recorder_type, request, response)

    def set_failed(self, error, *args, **kwargs):
        '''
        Is called when service executed wrongly.
        '''

        request = self._create_request(*args, **kwargs)
        self._attach_to_transaction(request)
        coordinator_services.set_failed(self._recorder_type, request, error)

    def _reverse_request(self, request):
        '''
        Reverses given service call.
        '''

        pass


def record(key, **options):
    '''
    Records outgoing services.

    @param str key: service unique key
    @keyword str recorder_type: recorder type
    @keyword bool should_be_reversed: should be reversed
    '''

    def record_decorator(f):
        '''
        Records given callable.
        '''

        wrapper = RequestCoordinatorWrapper(key, **options)

        def new_func(*args, **kwargs):
            """
            The function that creates a new command.
            """

            try:
                result = f(*args, **kwargs)
                wrapper.set_completed(result, *args, **kwargs)
                return result
            except Exception as error:
                wrapper.set_failed(error, *args, **kwargs)
                raise

        # Setting the new_function name...
        new_func.__name__ = f.__name__
        new_func.__module__ = f.__module__
        new_func.__doc__ = f.__doc__
        new_func.location = f.__module__

        record_decorator.__name__ = f.__name__
        record_decorator.__module__ = f.__module__

        return new_func

    return record_decorator