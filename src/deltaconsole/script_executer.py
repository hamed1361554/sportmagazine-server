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
Created on Dec 24, 2009
@author: Aidin Gharibnavaz

This module contains all of the tools we need to run
Python scripts inside the console.
'''

import re #Regular expression
import service_manager
import utils


class ScriptExecutionError(Exception):
    pass


def execute_script_file(file_to_execute):
    """Execute the script in the given file"""
    try:
        script_file = open(file_to_execute)
    except IOError, io_error:
        raise ScriptExecutionError("Couldn't open file:{filename}"
                                   "\n{error}".format(filename=file_to_execute,
                                                      error=io_error))
    script_content = script_file.read()
    script_content = _replace_commands_in_script(script_content)
    
    _execute_script(script_content)


def execute_script_from_interactive_shell():
    """Open an interactive shell, read the script from it,
    and execute the script.
    """
    script_content = ''
    user_input = raw_input('>>> ').rstrip()
    
    while user_input:
        script_content += '\n' + user_input
        user_input = raw_input('>>> ').rstrip()
    
    if not script_content:
        #Nothing is entered in the interactive shell.
        return
    
    _execute_script(script_content)


def _execute_script(script_content):
    """Execute the given script"""
    script_content = _replace_commands_in_script(script_content)
    
    #EXECUTER is used inside the script_content.
    command_executer = service_manager.CommandExecuter()
    EXECUTER = command_executer.execute_parsed_command 
    
    try:
        exec(script_content)
    except Exception, error:
        raise ScriptExecutionError(error)
    except KeyboardInterrupt:
        return

def _replace_commands_in_script(script_content):
    """Find and replace all of the commands (only server-side 
    commands) in the given script, by a Python expression that
    can be executed normally.
    
    @param script_content: Script to modify
    
    @return: Modified script
    """
    raw_commands_list = _find_all_commands_in_script(script_content)
    
    for raw_command in raw_commands_list:
        modified_command = _make_command(raw_command)
        script_content = script_content.replace(raw_command, modified_command)
    
    return script_content


def _find_all_commands_in_script(script_content):
    """Find all of the expression that match $...$ pattern.
    These are the server-side commands.
    
    @param script_content: Text to search
    
    @return: A list of all of the expressions that matched
             the pattern.
    """
    #Finding the pattern, using regular expression
    pattern = re.compile('\$.*\$', re.M)
    return pattern.findall(script_content)


def _make_command(raw_command):
    """Modify the given raw_command in a way that it can
    be executed normally, using service_manager.
    
    @param raw_command: The raw command in $...$ format
    
    @return: Modified command, that can be executed by Python
    """
    #Removing dollars in the given string.
    raw_command = raw_command.replace('$', '')
    
    command, arguments = _parse_command_string(raw_command)
    #EXECUTER will be define latter, just before the execution of the script.
    modified_command = "EXECUTER('{command}', {arguments})".format(
                                                            command=command,
                                                            arguments=arguments)
    return modified_command


def _parse_command_string(command_string):
    """Parse the given string, and make it ready for the execution.
    
    @param command_string: String to parse.
    
    @return: Parsed command and its arguemts as a tuple.
    """
    user_command, ignore_me, user_arguments = command_string.partition('(')
    
    user_arguments = user_arguments.rstrip()
    
    if not user_arguments.endswith(')'):
        raise ScriptExecutionError('Missing close paranthese')
    
    #Removing the last paranthese
    user_arguments = user_arguments[:len(user_arguments) - 1]
    
    return user_command, user_arguments

