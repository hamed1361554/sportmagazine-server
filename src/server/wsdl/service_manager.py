# DeltaConsole, A console for DeltaPy applications.
# Copyright (C) 2009-2011  Aidin Gharibnavaz <aidin@aidinhut.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on Nov 2009
@author: Aidin Gharibnavaz

A module for handling the services.
'''

import sys
import os
import time
#For letting user to work with datetime easily.
from datetime import (datetime, timedelta)
import xmlrpclib
import Pyro.core

try:
    import Ice
    import ice_utils
    ICE_ENABLED = True
except ImportError:
    ICE_ENABLED = False

import utils
import output_handler
import local_executer
from type_convertor import TypeConvertor

class ClientTypeConvertor(TypeConvertor):
    
    def internal_convert(self, obj):
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8')
        if isinstance(obj, str):
            obj = obj.decode('cp1256').encode('utf-8')
        
        return obj
    
    def external_convert(self, obj):
        return obj

#Create Ice server class only if it was available on the system.
if ICE_ENABLED:
    class IceServer(object):
        def __init__(self, server_address, server_port):
            server_url = 'ice:tcp -h {host} -p {port} -z'.format(host=server_address,
                                                              port=server_port)
            try:
                properties = Ice.createProperties()
                properties.setProperty('Ice.MessageSizeMax', '10240')
                properties.setProperty('Ice.Override.Compress', '1')
                                
                data = Ice.InitializationData()
                data.properties = properties
                communicator = Ice.initialize(data)
                self._server_proxy = ice_utils.IIceDispatcherPrx.checkedCast(
                                             communicator.stringToProxy(server_url))
            except Ice.Exception as ice_error:
                print ice_error
                sys.exit(30)

            self._user = None
            self._ticket = None
        
        def login(self, user, password, **options):
            """Login to the server"""
            converted_options = ice_utils.dict_to_ddict(options)
            user = ice_utils.object_to_dobject(user)
            password = ice_utils.object_to_dobject(password)

            self._user = user
            self._ticket = self._server_proxy.login(user, password, converted_options)
            
            if self._ticket in (None, ''):
                raise Exception("Could not login to the server.")

        def execute(self, command, *args, **kargs):
            """Execute the given command at server."""
            if self._ticket in (None, ''):
                return "You're not login to the server yet"
            t_args = None
            if args:
                t_args = ice_utils.list_to_dlist(list(args))
            t_kargs = ice_utils.dict_to_ddict(kargs)

            command = ice_utils.object_to_dobject(command)

            result =  self._server_proxy.execute(self._ticket,
                                                 self._user,
                                                 command,
                                                 t_args,
                                                 t_kargs)
            return ice_utils.dlist_to_list([result])[0]

        def logoff(self, user):
            """Log off from the server"""
            user = ice_utils.object_to_dobject(user)

            self._server_proxy.logout(self._ticket, user)
            self._ticket = None

class XmlrpcServer(object):

    def __init__(self, server_address, server_port, service_name):
        """
        @param server_address : Address of the server
        @param server_port    : Port server is listening at.
        @param service_name: Name of the service (will set at the server-side)
        """
        server_url = "http://{address}:{port}".format(address=server_address,
                                                      port = server_port)
        self._server_proxy = xmlrpclib.Server(server_url)
        self._service_name = service_name
        self._ticket = None
        self._user = None
        self._type_convertor = ClientTypeConvertor()
        
    def login(self, user, password, **options):
        """Login to the server."""
        self._user = user
        method = getattr(self._server_proxy, 
                         "{0}.login".format(self._service_name))
        self._ticket = method(user, password)
        if self._ticket in (None, ''):
            raise Exception("Could not login to the server.")

    def execute(self, command , *args, **kargs):
        """Execute a command."""
        if self._ticket in (None, ''):
            return "You're not login to the server yet"
        
        method = getattr(self._server_proxy,
                         "{0}.execute".format(self._service_name))
        result =  method(self._ticket, 
                         self._user,
                         command, 
                         *args, 
                         **kargs)
        
        return self._type_convertor.to_internal(result)

    def logoff(self, user):
        """Logoff from the server."""
        method = getattr(self._server_proxy,
                         "{0}.logout".format(self._service_name))
        method(self._ticket, user)
        self._ticket = None


class PyroServer(object):
    
    def __init__(self, server_address, server_port):
        """
        @param server_address : Address of the server
        @param server_port    : Port server is listening at.
        """
        Pyro.config.PYRO_MULTITHREADED = 1
        Pyro.core.initClient()
        
        url = 'PYROLOC://{address}:{port}/pyro'.format(address = server_address,
                                                       port = server_port)        
        self._server_proxy = Pyro.core.getProxyForURI(url)
        
        self._ticket = None
        self._user = None
        self._type_convertor = ClientTypeConvertor()

    def login(self, user, password, **options):
        """Login to the server."""
        self._user = user
        self._ticket = self._server_proxy.login(user, password, **options)
        if self._ticket in (None, ''):
            raise Exception("Could not login to the server.")

    def execute(self, command, *args, **kargs):
        """Execute a command at the server."""
        if self._ticket in (None, ''):
            return "You're not login to the server yet."
        result =  self._server_proxy.execute(self._ticket,
                                             self._user,
                                             command,
                                             *args,
                                             **kargs)
        return self._type_convertor.to_internal(result)

    def execute_ex(self, command, context=None, *args, **kargs):
        """Execute a command at the server."""
        if self._ticket in (None, ''):
            return "You're not login to the server yet."
        result = \
            self._server_proxy.execute_ex({'ticket': self._ticket,
                                           'user_name': self._user,
                                           'command_key': command,
                                           'command_args': args,
                                           'command_kwargs': kargs,
                                           'context': context})
        return self._type_convertor.to_internal(result)
        
    def logoff(self, user):
        """Logoff from the server."""
        self._server_proxy.logout(self._ticket, user)
        self._ticket = None


class HookManager(object):
    """A class to manage execution hooks."""
    def __init__(self):
        self._before_execution_hooks = []
        self._after_execution_hooks = []

    def register_before_execution_hook(self, hook):
        """Register a hook to run before execution of a command."""
        self._before_execution_hooks.append(hook)

    def register_after_execution_hook(self, hook):
        """Register a hook to run after execution of a command."""
        self._after_execution_hooks.append(hook)
    
    def execute_before_execution_hooks(self, raw_command_string):
        """Execute all of the hooks that registered to execute
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
        """Execute all of the hooks that registered to execute
        after the execution of the command.
        """
        final_result = result
        for hook in self._after_execution_hooks:
            hook_result = hook(raw_command, executed_command, final_result)
            if hook_result is not None:
                final_result = hook_result
        return final_result

class CommandExecuter(object):
    """This can execute server or local commands.
    Note that it's a singleton class.
    """
    _single_instance = None #The only instance of this class.
    __configurations = None
    __hook_manager = None

    def __new__(cls, *args, **kwargs):
        #Check to see if a __single already exists in this class.
        #We compare type of the cls and our single_instance, so subclasses
        #can have their own single_instance.
        if not isinstance(cls._single_instance, cls):
            cls._single_instance = object.__new__(cls, *args, **kwargs)
        return cls._single_instance

    def configure(self, arguments):
        """Set the executer options.
        This will terminate the program, if the specified arguments
        wasn't valid.
        
        @param arguments: command line arguements, as a dictionary.
        """
        self.__configurations = arguments
        self._user = ''

        if self.__hook_manager is None:
            self.__hook_manager = HookManager()
        
        if arguments.protocol.upper() == 'XMLRPC':
            self._server_proxy = XmlrpcServer(arguments.host,
                                              arguments.port,
                                              arguments.service_name)
        elif arguments.protocol.upper() == 'PYRO':
            self._server_proxy = PyroServer(arguments.host,
                                            arguments.port)
        elif arguments.protocol.upper() == 'ICE' and ICE_ENABLED:
            self._server_proxy = IceServer(arguments.host,
                                           arguments.port)
        else:
            print 'Unkown protocol {0}'.format(arguments.protocol)
            sys.exit(-1)

    def register_before_execution_hook(self, hook):
        """Register a hook to run before execution of a command.
        
        Raw command string will be passes to this hook, and if
        it returns anything, the command string will be replaced
        by the returned value.
        """
        self.__hook_manager.register_before_execution_hook(hook)

    def register_after_execution_hook(self, hook):
        """Register a hook to run after execution of a command.
        
        The parameters that will be passed to this hook are:
            raw_command_string: Raw command string as user inputed.
            executed_command_string: Command string that really
                executed.
            result: Result of the command.
        """
        self.__hook_manager.register_after_execution_hook(hook)

    def login(self, user_name, password, **options):
        """Login to the server.
        
        @param user_name: User name, should be in format 'branchcode-usercode'
        @param password: Password of the user
        """
        #Reconnect to the server.
        self.configure(self.__configurations)
        
        self._server_proxy.login(user_name, password, **options)
        self._user = user_name

    def logoff(self):
        """Logoff from the server"""
        self._server_proxy.logoff(self._user)

    def execute_command(self, command_string):
        """Execute a command, at server-side or locally,
        and print out it's result.
        
        @param command_string: The string that user input.
        
        @return: Result of the command. None if there was no result.
        """
        original_command_string = command_string

        command_string = \
            self.__hook_manager.execute_before_execution_hooks(command_string)

        if utils.is_local_command(command_string):
            command, arguments = utils.local_command_parser(command_string)
            
            if not command:
                return
            
            result = local_executer.Execute(command, arguments)
            
            self.__hook_manager.execute_after_execution_hooks(
                original_command_string, command_string, result)
            
            return result
        
        else:
            command, arguments, context = utils.server_command_parser(command_string)

            if not command:
                return

            #By executing the command like this, Python is responsible for
            #parsing the arguments.
            if len(arguments) > 0:
                exec('result = self._server_proxy.execute'
                     '("{command}", {arguments})'.format(command=command,
                                                         arguments=arguments))
            else:
                exec('result = self._server_proxy.execute'
                     '("{command}")'.format(command=command))
            
            result = self.__hook_manager.execute_after_execution_hooks(
                           original_command_string, command_string, result)

            return result

    def execute_command_ex(self, command_string):
        """Execute a command, at server-side or locally,
        and print out it's result.

        @param command_string: The string that user input.

        @return: Result of the command. None if there was no result.
        """
        original_command_string = command_string

        command_string = \
            self.__hook_manager.execute_before_execution_hooks(command_string)

        if utils.is_local_command(command_string):
            command, arguments = utils.local_command_parser(command_string)

            if not command:
                return

            result = local_executer.Execute(command, arguments)

            self.__hook_manager.execute_after_execution_hooks(
                original_command_string, command_string, result)

            return result

        else:
            command, arguments, context = utils.server_command_parser(command_string)

            if not command:
                return

            #By executing the command like this, Python is responsible for
            #parsing the arguments.
            if len(arguments) > 0:
                exec('result = self._server_proxy.execute_ex'
                     '("{command}", {context},{arguments})'.format(command=command,
                                                                   context=context,
                                                                   arguments=arguments))
            else:
                exec('result = self._server_proxy.execute_ex'
                     '("{command}", {context})'.format(command=command,
                                                       context=context))

            result = self.__hook_manager.execute_after_execution_hooks(
                           original_command_string, command_string, result)

            return result

    def execute_parsed_command(self, command, *args, **kargs):
        """Execute an already parsed command, at the server-side."""
        if not command:
            return
        start_time = time.time()
        result = self._server_proxy.execute(command, *args, **kargs)
        end_time = time.time()
        
        output_handler.output_printer(result)
        utils.print_elapsed_time(start_time, end_time)


    def __getattr__(self, attr_name):
        return self._single_instance.__dict__[attr_name]


    def __setattr__(self, attr_name, attr_value):
        self._single_instance.__dict__[attr_name] = attr_value

