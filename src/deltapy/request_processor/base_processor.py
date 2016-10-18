'''
Created on Feb 8, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import signal
import datetime
import time
import traceback

from deltapy.core import DeltaObject, DynamicObject
from deltapy.security.authentication.services import authenticate
from deltapy.security.authentication.authenticator import IP_ADDRESS_OPTION_KEY
from deltapy.event_system.decorators import delta_event
from deltapy.request_processor.services import get_timeout
from deltapy.request_processor.response import Response
from deltapy.request_processor.services import get_request_processor_hooks
from deltapy.request_processor.request import ClientRequest
import deltapy.security.authentication.services as authentication_services
import deltapy.commander.services as commander_services
import deltapy.logging.services as logging_services
import deltapy.unique_id.services as unique_id_services
import deltapy.request_processor.helper.services as request_processor_helper_services


LOGGER = logging_services.get_logger(name='requestprocessor')

def handle_request(raw_request, **options):
    '''
    Processes the request.
    
    @param request: client request
    
    @return: Response
    '''
    request_dict = raw_request.get_request_dict()

    # Converting client request to the type we expected.
    type_converter = raw_request.get_converter()
    if type_converter is not None:
        request_dict = type_converter.to_internal(request_dict)
        options = type_converter.to_internal(options)
    
    # Filling missing fields.
    if request_dict.get('id') is None:
        request_dict['id'] = unique_id_services.get_id('uuid')
    if request_dict.get('request_date') is None:
        request_dict['request_date'] = datetime.datetime.now()
    
    client_request = ClientRequest.from_dict(request_dict)

    # logging request.
    process_start_time = time.time()
    LOGGER.info(('[{command}],[{request_id}],[{user}@{ip}:{ticket}],trace_id[{trace_id}] received. '
                 'params: [{params}], context: [{context}]').format(command=client_request.command_key,
                                                                    request_id=client_request.id,
                                                                    trace_id=client_request.trace_id,
                                                                    user=client_request.user_name,
                                                                    ip=client_request.ip,
                                                                    ticket=client_request.ticket,
                                                                    params=(client_request.command_args, client_request.command_kwargs),
                                                                    context=client_request.context))

    # Authenticating sessions
    authentication_options = {}
    if client_request.context is not None and IP_ADDRESS_OPTION_KEY in client_request.context:
        authentication_options[IP_ADDRESS_OPTION_KEY] = client_request.context[IP_ADDRESS_OPTION_KEY]

    session = authenticate(client_request.ticket,
                           client_request.user_name,
                           client_ip=client_request.ip,
                           **authentication_options)

    # Activating session
    session.active(client_request)

    # Getting timeout value
    timeout = client_request.timeout

    if timeout is None:
        timeout = get_timeout()
        client_request.timeout = timeout

    try:
        # Getting command parameters
        _args = client_request.command_args
        if len(client_request.command_args) == 1:
            if isinstance(client_request.command_args[0], tuple):
                _args = client_request.command_args[0]

        # Setting request timeout in current thread
        request_processor_helper_services.set_request_timeout(timeout)

        # Making a loop and informing hooks to prepare before executing the service
        for hook in get_request_processor_hooks():
            hook.on_process(client_request, **options)

        # Executing the command
        result = \
            commander_services.execute(client_request.command_key, *_args, **client_request.command_kwargs)

        # Creating response object
        response = Response(client_request,
                            result,
                            session.get_call_context())

        # Making a loop and informing hooks to complete their actions
        for hook in reversed(get_request_processor_hooks()):
            hook.on_process_completed(client_request, response, **options)

        # Logging result.
        LOGGER.info(('[{command}],[{request_id}],[{user}@{ip}:{ticket}],trace_id[{trace_id}] '
                     'executed in time [{execution_time}]').format(command=client_request.command_key,
                                                                   request_id=client_request.id,
                                                                   trace_id=client_request.trace_id,
                                                                   user=client_request.user_name,
                                                                   ip=client_request.ip,
                                                                   ticket=client_request.ticket,
                                                                   execution_time=time.time() - process_start_time))
        LOGGER.debug(('[{command}],[{request_id}],[{user}@{ip}:{ticket}],trace_id[{trace_id}] executed. '
                      'result: [{result}], context: [{context}]').format(command=client_request.command_key,
                                                                         request_id=client_request.id,
                                                                         trace_id=client_request.trace_id,
                                                                         user=client_request.user_name,
                                                                         ip=client_request.ip,
                                                                         ticket=client_request.ticket,
                                                                         result=result,
                                                                         context=response.context))

        # Converting the result to the type Communicator expected.
        if type_converter is not None:
            response = type_converter.to_external(response)

        return response

    except Exception as error:
        LOGGER.error('Error while executing [{command}],[{request_id}]: [{traceback}]'.format(command=client_request.command_key,
                                                                                              request_id=client_request.id,
                                                                                              traceback=traceback.format_exc()))
        # Making a loop and informing hooks to handle the occurred error
        for hook in get_request_processor_hooks():
            hook.on_process_failed(client_request, error, **options)
        raise

    finally:
        # Deactivating alarm
        if timeout is not None and timeout > 0:######insert
            signal.alarm(0)

        # Cleaning up the session
        session.cleanup()


# Note: This is done this way, in order to apply changes of RFC-32182 with
#  minimum possible cost. This should be re-factor completely, later.
@delta_event('security.login')
def login_event(self, listener, ip, user_name, password, **options):
    return options['result']

def login(login_request):
    """
    Authenticates the given credentials and returns login information.

    @param instance login_request: Raw request recevied from client.

    @return: login data
    @rtype: instance
    """
    converter = login_request.get_converter()

    if converter is not None:
        login_request = converter.to_internal(login_request.get_request_dict())
    else:
        login_request = login_request.get_request_dict()

    try:
        # For calculating execution time.
        process_start_time = time.time()

        if login_request.get('options') is None:
            login_request['options'] = {}

        login_request['options']['client_ip'] = login_request['ip']

        login_info = DynamicObject()
        login_info.ticket = authentication_services.login(login_request['user_name'],
                                                          login_request['password'],
                                                          **login_request['options'])
        login_info.data = {}
        login_info.login_date = datetime.datetime.now()

        # Note: This should be refactored later. (see comment on `login_event').
        login_event(None, None,
                    login_request['ip'],
                    login_request['user_name'],
                    login_request['password'],
                    result=login_info,
                    **login_request['options'])

        LOGGER.info('User[{user}@{ip}],Channel[{channel}],Ticket[{ticket}] logged in. Time: [{execution_time}]'.format(user=login_request['user_name'],
                                                                                                                       ip=login_request['ip'],
                                                                                                                       channel=login_request['options'].get('channel'),
                                                                                                                       ticket=login_info['ticket'],
                                                                                                                       execution_time=time.time() - process_start_time))

        if converter is not None:
            login_info = converter.to_external(login_info)

        return login_info

    except Exception as error:
        LOGGER.error('User[{user}@{ip}],Channel[{channel}] Login failed: {error}'.format(user=login_request['user_name'],
                                                                                                          ip=login_request['ip'],
                                                                                                          channel=login_request['options'].get('channel'),
                                                                                                          error=str(error)))
        raise

def logout(logout_request):
    '''
    Logout the user from application.
    
    @param instance logout_request: Raw request received from client.
    '''
    converter = logout_request.get_converter()
    
    if converter is not None:
        logout_request = converter.to_internal(logout_request.get_request_dict())
    else:
        logout_request = logout_request.get_request_dict()

    # For calculating execution time.
    process_start_time = time.time()

    if logout_request.get('options') is None:
        logout_request['options'] = {}
    
    logout_request['options']['client_ip'] = logout_request['ip']
    
    authentication_services.logout(logout_request['ticket'],
                                   logout_request['user_name'],
                                   **logout_request['options'])

    LOGGER.info('User[{user}@{ip}],Channel[{channel}],Ticket[{ticket}] logged out. Time: [{execution_time}]'.format(user=logout_request['user_name'],
                                                                                                                    ip=logout_request['ip'],
                                                                                                                    channel=logout_request['options'].get('channel'),
                                                                                                                    ticket=logout_request['ticket'],
                                                                                                                    execution_time=time.time() - process_start_time))


class RequestProcessorBase(DeltaObject):
    '''
    Request processor base.
    '''
    
    def __init__(self, name):
        DeltaObject.__init__(self)
        self._set_name_(name)
        self._params = {}
    
    def configure(self, params):
        '''
        Configures request processor.
        @param params:
        '''

        self._params = params
    
    def process(self, 
                request,
                **options):
        '''
        Processes the request.
        
        @param request: client request
        
        @return: Response
        '''    

    def login(self, login_request):
        """
        Authenticates the given credentials and returns login information.
    
        @param instance login_request: Raw request recevied from client.
    
        @return: login data
        @rtype: instance
        """

    def logout(self, logout_request):
        '''
        Logout the user from application.
        
        @param instance logout_request: Raw request received from client.
        '''

    def get_params(self):
        '''
        Returns request processor parameters.
        '''
        
        return self._params
    
    def terminate(self):
        '''
        Terminates current request processor.
        '''

        raise NotImplementedError()

    def resize(self, size):
        '''
        @param size:
        '''
        pass