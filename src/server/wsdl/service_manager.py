"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

import sys
import time
import Pyro.core

from server.wsdl.type_convertor import TypeConvertor


class ClientTypeConvertor(TypeConvertor):

    def internal_convert(self, obj):
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        if isinstance(obj, str):
            obj = obj.decode('cp1256').encode('utf-8')

        return obj

    def external_convert(self, obj):
        return obj


class PyroServer(object):
    """
    Pyro Server
    """
    
    def __init__(self, server_address, server_port):
        """
        @param server_address : Address of the server
        @param server_port    : Port server is listening at.
        """

        Pyro.config.PYRO_MULTITHREADED = 1
        Pyro.core.initClient()
        
        url = 'PYROLOC://{address}:{port}/pyro'.format(address=server_address,
                                                       port=server_port)
        self._server_proxy = Pyro.core.getProxyForURI(url)

        self._type_converter = TypeConvertor()

    def login(self, user, password, **options):
        """
        Login to the server.
        """

        ticket = self._server_proxy.login(user, password, **options)
        if ticket in (None, ''):
            raise Exception("Could not login to the server.")
        return ticket

    def execute(self, ticket, user, command, *args, **kargs):
        """
        Execute a command at the server.
        """

        result = self._server_proxy.execute(ticket,
                                            user,
                                            command,
                                            *args,
                                            **kargs)
        return self._type_converter.to_internal(result)

    def execute_ex(self, ticket, user, command, context=None, *args, **kargs):
        """
        Execute a command at the server.
        """

        result = \
            self._server_proxy.execute_ex({'ticket': ticket,
                                           'user_name': user,
                                           'command_key': command,
                                           'command_args': args,
                                           'command_kwargs': kargs,
                                           'context': context})
        return self._type_converter.to_internal(result)
        
    def logoff(self, ticket, user):
        """
        Logoff from the server.
        """

        self._server_proxy.logout(ticket, user)


class HookManager(object):
    """
    class to manage execution hooks.
    """

    def __init__(self):
        self._before_execution_hooks = []
        self._after_execution_hooks = []

    def register_before_execution_hook(self, hook):
        """
        Register a hook to run before execution of a command.
        """

        self._before_execution_hooks.append(hook)

    def register_after_execution_hook(self, hook):
        """
        Register a hook to run after execution of a command.
        """

        self._after_execution_hooks.append(hook)
    
    def execute_before_execution_hooks(self, raw_command_string):
        """
        Execute all of the hooks that registered to execute
        before the execution of the command.
        """

        raw_command = raw_command_string
        
        for hook in self._before_execution_hooks:
            new_raw_command = hook(raw_command)
            if new_raw_command not in (None, ''):
                raw_command = new_raw_command
        
        return raw_command

    def execute_after_execution_hooks(self, raw_command,
                                      executed_command,
                                      result):
        """
        Execute all of the hooks that registered to execute
        after the execution of the command.
        """

        final_result = result
        for hook in self._after_execution_hooks:
            hook_result = hook(raw_command, executed_command, final_result)
            if hook_result is not None:
                final_result = hook_result
        return final_result
