'''
Created on Feb 27, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

import fnmatch

from deltapy.core import DeltaObject, DeltaEnum, DeltaEnumValue, DynamicObject
from deltapy.request_processor.services import register_request_processor_hook
from deltapy.request_processor.coordinator.request_processor_hook import TransactionCoordinatorRequestProcessorManagerHook
from deltapy.security.channel.services import get_current_channel_id

import deltapy.logging.services as logging_services
import deltapy.request_processor.coordinator.recorder.services as request_recorder_services
import deltapy.security.channel.services as channel_services
import deltapy.commander.services as commander_services

class TransactionCoordinator(DeltaObject):
    
    LOGGER = logging_services.get_logger(name='request.coordinator')
    
    class StateEnum(DeltaEnum):
        RECIEVED = DeltaEnumValue(0, 'Received')
        COMPLETED = DeltaEnumValue(1, 'Completed')
        FAILED = DeltaEnumValue(2, 'Failed')
        
    def __init__(self):
        self._channels = {}
        self.load()
        register_request_processor_hook(TransactionCoordinatorRequestProcessorManagerHook())

    def load(self):
        '''
        Loads activated channels and services. 
        '''

        self._channels = {}

        all_commands = []
        for command in commander_services.get_commands():
            all_commands.append(command.get_key())

        if channel_services.is_enable():
            for channel in channel_services.get_all():
                self._add_channel_services(channel, all_commands=all_commands)

    def add_channel(self, channel_id):
        """
        Adds a channel to coordinator.

        @param str channel_id: channel id
        """

        all_commands = []
        for command in commander_services.get_commands():
            all_commands.append(command.get_key())

        if channel_services.is_enable():
            channel = channel_services.get(channel_id)
            self._add_channel_services(channel, all_commands=all_commands)

    def _add_channel_services(self, channel, **options):
        """
        Registers allowed services for given channel.

        @param dict channel: channel information

        @keyword list all_commands: List of commands` key
        @type all_commands: list(str command_key: command key)
        """

        # Getting command from options
        all_commands = options.get('all_commands')

        if channel is None:
            return

        # IF command is not given, getting commands key
        if all_commands is None or len(all_commands) == 0:
            for command in commander_services.get_commands():
                all_commands.append(command.get_key())

        # Registering channel services
        if 'recordable_services' in channel:
            service_patterns = channel.recordable_services.replace(';', ',').split(',')
            for pattern in service_patterns:
                for service_id in all_commands:
                    if fnmatch.fnmatch(service_id, pattern.strip()):
                        self.activate_service(channel.id, service_id)
            enable_recording = channel.get('enable_recording')
            if enable_recording:
                self.activate_channel(channel.id)
            else:
                self.deactivate_channel(channel.id)
                        
    def get_request_state(self, request_id):
        '''
        Returns state of specified request.
        
        @param str request_id: request ID
        
        @rtype: int
        @note: 
            0: Received
            1: Completed
            2: Failed
        @return: request state
        '''
        
        return request_recorder_services.get_request_state(request_id)
        
    def get_transaction_state(self, transaction_id):
        '''
        Returns transaction state.
        
        @param str transaction_id: transaction ID
        
        @rtype: int
        @note: 
            0: Received
            1: Completed
            2: Failed
        @return: transaction state
        '''

    def get_transaction_detail(self, transaction_id):
        '''
        Returns detail information of the specified transaction.
        
        @param str transaction_id: transaction ID
        
        @rtype: dict(str transaction_id: transaction ID
                     int state: transaction state,
                     datetime start_date: start date of transaction,
                     str user_id: user ID,
                     list requests: requests regarding to the transaction)
        @type requests: dict(str request_id: request ID,
                             int state: request state,
                             object input: request input,
                             object result: request result)
                             
        @return: transaction detail
        '''

    def _get_channel_info(self, channel_id):
        '''
        Returns channel information.
        
        @param str channel_id: channel ID
        
        @rtype: dict(bool enable,
                     list services)
        @type services: list
        @return: channel information
        '''
        
        channel = self._channels.get(channel_id)
        if channel is None:
            channel = DynamicObject(enabled=False, services=[])
            self._channels[channel_id] = channel
        return channel

    def activate_channel(self, channel_id):
        '''
        Activates transaction coordination on the given channel. 
        
        @param str channel_id: channel ID
        '''
        
        channel = self._get_channel_info(channel_id)
        if not channel.enabled:
            channel.enabled = True
    
    def activate_service(self, channel_id, service_id):
        '''
        Activates transaction coordination on the given service.

        @param str channel_id: channel ID
        @param str service_id: service ID
        '''
        
        channel = self._get_channel_info(channel_id)
        if service_id not in channel.services:
            channel.services.append(service_id)
        
    def deactivate_channel(self, channel_id):
        '''
        Deativates transaction coordination on the given channel. 
        
        @param str channel_id: channel ID
        '''
        
        channel = self._get_channel_info(channel_id)
        if channel.enabled:
            channel.enabled = False

    def deactivate_service(self, channel_id, service_id):
        '''
        Dectivates transaction coordination on the given service.
        
        @param str channel_id: channel ID
        @param str service_id: service ID
        '''
        
        channel = self._get_channel_info(channel_id)
        if service_id in channel.services:
            channel.services.pop(service_id)
            
    def is_required_to_record_request(self, request):
        '''
        Returns True if the request must be recorded.
        
        @param ClientRequest request: request instance
        
        @rtype: bool
        @return: True or False
        '''

        channel_id = get_current_channel_id()
        channel = self._get_channel_info(channel_id)
        if channel.enabled:
            if request.command_key in channel.services:
                return True
        return False

    def record_request(self, request, **options):
        '''
        Records a request data using the given information.
        
        @param dict request: request data
        @type request: dict(str id: request ID,
                            str transaction_id: transaction ID,
                            str user_name: user name,
                            str ip: client IP,
                            datetime recieve_date: receive date,
                            datetime request_date: request date from client)
        '''

        if self.is_required_to_record_request(request):
            request_recorder_services.record(request)
        
        
    def set_completed(self, request, **options):
        '''
        Completes the state of the given request.
        
        @param str request_id: request ID
        @param request_id: request ID
        '''
        
        if self.is_required_to_record_request(request):
            request_recorder_services.set_completed(request.id)
        
    def set_failed(self, request, error, **options):
        '''
        Sets the state of the given request to failed.
        
        @param str request_id: request ID
        @param str error: error description 
        '''

        if self.is_required_to_record_request(request):
            request = request_recorder_services.try_get(request.id)
            if request is not None:
                request_recorder_services.set_failed(request.id, error)
    