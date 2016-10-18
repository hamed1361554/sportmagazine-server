'''
Created on Jun 25, 2016

@author: Hamed
'''

from deltapy.commander.hook import CommandExecutionHook

import deltapy.logging.services as logging_services
import deltapy.security.session.services as session_services
import deltapy.request_processor.coordinator.services as coordinator_services


class TransactionCoordinatorCommandExecutionHook(CommandExecutionHook):
    '''
    Transaction Coordinator Command Execution Hook
    '''

    LOGGER = logging_services.get_logger(name='request.coordinator')

    def before_execute(self, commander, command, *args, **kargs):
        '''
        This method will be called before command execution.

        @param commander: commander
        @param command: command
        '''

        if not self._is_required_to_record_request(command):
            return

        request = session_services.get_current_session().get_client_request()
        coordinator_services.record_request(command.get_option('recorder_type'), request)
        logging_services.debug('Request [{0}] for service [{1}] recorded.'.format(request.id, command.get_key()))

    def after_execute(self, commander, command, result, *args, **kargs):
        '''
        This method will be called after command execution.

        @param commander: commander
        @param command: command
        @param result: command execution result
        '''

        if not self._is_required_to_record_request(command):
            return

        request = session_services.get_current_session().get_client_request()
        coordinator_services.set_completed(command.get_option('recorder_type'), request, result)
        logging_services.debug('Request [{0}] for service [{1}] completed.'.format(request.id, command.get_key()))

    def exception(self, commander, command, error, *args, **kargs):
        '''
        This method will be called whenever an exception occurred during executing a command.

        @param commander: commander
        @param command: command
        @param error: exception instance
        '''

        if not self._is_required_to_record_request(command):
            return

        request = session_services.get_current_session().get_client_request()
        coordinator_services.set_failed(command.get_option('recorder_type'), request, error)
        logging_services.debug('Request [{0}] for service [{1}] failed.'.format(request.id, command.get_key()))

    def _is_required_to_record_request(self, command):
        '''
        Returns True if the request must be recorded.

        @param Command command: command instance

        @rtype: bool
        @return: True or False
        '''

        if not self.is_enable():
            return False

        recorder_type = command.get_option('recorder_type')
        return recorder_type not in (None, '')