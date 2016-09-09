#!/usr/bin/env python
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

Executer module of Delta Console
'''
__author__ = 'Aidin Gharibnavaz'
__version__ = '3.4.1'

import sys
import os
import time
import warnings
import getpass
import xmlrpclib
import service_manager
import utils
import prompt_handler
import output_handler
from utils import SETTINGS_DICT

CHANNEL_NAME = 'DELTACONSOLE'

def load_hooks():
    """Loads (imports) all of the modules in `hooks' package."""
    #XXX: Ugly code. Should be reviewed.
    hooks_package_path = os.path.join(
        os.path.abspath(os.path.dirname(service_manager.__file__)),
        'hooks')
    for root, dirs, files in os.walk(hooks_package_path):
        for hookfile in files:
            if hookfile.endswith('.py'):
                try:
                    module_name = 'hooks.{0}'.format(hookfile[:-3])
                    module = __import__(module_name, globals(), locals(), [])
                except ImportError:
                    raise
                    continue


command_line_args = utils.get_configurations(sys.argv)

executer = service_manager.CommandExecuter()
executer.configure(command_line_args)
load_hooks()

utils.print_welcome(__version__)

#Getting username and password.
try:
    if command_line_args.user is None:
        user_name = raw_input("User: ")
    else:
        user_name = command_line_args.user
    
    password = getpass.getpass()
    #Login to the server.
    #executer.login(user_name, password, channel=CHANNEL_NAME)
    executer.login(user_name, password)

except xmlrpclib.Fault, xmlrpc_fault_error:
    #XMLRPC's fault messages are ugly, so we have to format them.
    print utils.ANSICOLORS.FRED % \
          utils.format_xmlrpc_fault_error(xmlrpc_fault_error.faultString)
#Exiting nicely at interruption.
except (KeyboardInterrupt, EOFError):
    print 
    sys.exit()
except Exception, other_errors:
    print utils.ANSICOLORS.FRED % other_errors


#Enabling readline, only if it's available.
#NOTE: I put this line here for two reasons: First, user must be logged in to
#      the server, so readline_handler can get the command's list from the 
#      server.
#      Second, login info shouldn't be saved in history, and history entries
#      shouldn't available at the login time.
import readline_handler


#Get and execute user's commands.
while True:
    try:
        raw_command = raw_input(prompt_handler.get_prompt_string())
        
        if not raw_command.strip():#Just an empty line.
            continue

        result = None
        start_time = time.time()

        if SETTINGS_DICT['debugging']:
            result = executer.execute_command_ex(raw_command)
        else:
            result = executer.execute_command(raw_command)
        end_time = time.time()

        output_handler.output_printer(result)
        if not utils.is_local_command(raw_command):
            #We do not print elapsed time for local commands.
            utils.print_elapsed_time(start_time, end_time)
    
    except xmlrpclib.Fault, xmlrpc_fault_error:
        #XMLRPC's errors are so ugly. So we have to format it.
        print utils.ANSICOLORS.FRED % \
            utils.format_xmlrpc_fault_error(xmlrpc_fault_error.faultString)
    
    except (KeyboardInterrupt, EOFError):
        print
        print utils.ANSICOLORS.FYELLOW % " * Exiting ..."
        print
        
        #Trying to logout.
        try:
            executer.logoff()
        except Exception:
            #In case of user didn't login before.
            pass
        
        sys.exit()

    except SyntaxError as ex:
        print utils.ANSICOLORS.FRED % ex.msg

    except Exception, other_error:
        # There's no way to print out an exception with unicode message.
        # That's why we done this.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            error_message = other_error.message
            if isinstance(error_message, unicode):
                error_message = error_message.encode('utf-8')
            print utils.ANSICOLORS.FRED % error_message

