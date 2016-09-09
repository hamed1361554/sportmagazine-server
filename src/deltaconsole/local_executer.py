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

This module contains functions for executing local commands.
'''

import os
import time
import getpass
import utils
import script_executer
from decorators import (local_command, setting_handler)

#This maps command names to their functions.
LOCAL_COMMANDS = {}
#This maps Set commands to its handlerer.
SETTING_FUNCTIONS = {}


class ExecutionError(Exception):
    pass


# NOTE: Docstrings of the functions will appear as their help messages.
#       That's why they're didn't wrote in Pythonic style.

#====================SUPPORTED COMMANDS============================

@local_command('set')
def _set(arguments):
    """
    You can use this function for set an option.
    
    Example: set timing off
    """
    
    if len(arguments) < 2:
        raise ExecutionError("'set' takes at least two argument")
    
    if not arguments[0] in SETTING_FUNCTIONS:
        raise ExecutionError("Don't know how to set {0}".format(arguments[0]))
    
    return SETTING_FUNCTIONS[arguments[0]](arguments[1:])
    

@local_command('using')
def _using(arguments):
    """
    This is a type-saving command!
    Using this command, You can set a prefix for all of the
    server-commands in the console.
    
    For example by typing `using security', a `security.' will
    add before every command you're type, and you do not have
    to type `security' over and over again.
    
    By invoking 'using' without any parameter, you will get back
    to the normal mode. 
    """
    if len(arguments) > 1:
        raise ExecutionError('_using takes at most one argument')
    
    if len(arguments) == 0 or arguments[0] in ('/', '.'):
        #Clear the prefixes.
        utils.SETTINGS_DICT['command_prefix'] = ''
        return ' '
    
    if arguments[0] in ('//', '..'):
        #Getting one level back
        old_prefix = utils.SETTINGS_DICT['command_prefix']
        #Finding the last dot, just before the one at the end of the prefix
        last_dot_index = old_prefix.rfind('.', 0, len(old_prefix) - 1)
        if last_dot_index == -1:
            #There was only one word in prefix, clearing it.
            utils.SETTINGS_DICT['command_prefix'] = ''
        else:
            #Remove the last word from prefix, but keep the last dot.
            utils.SETTINGS_DICT['command_prefix'] = \
                utils.SETTINGS_DICT['command_prefix'][:last_dot_index + 1]
        return ' '
    
    #Append the given prefix to the old one.
    prefix = arguments[0]
    prefix = prefix.strip()
    if not prefix.endswith('.'):
        prefix += '.'
    
    utils.SETTINGS_DICT['command_prefix'] += prefix
    return ' '


@local_command('/')
def _clear_prefix(arguments):
    """
    Clear the prefix (shortcut to 'using /')
    """
    if len(arguments) != 0:
        raise ExecutionError("You can't pass arguments to '/' command")
        
    return _using(('/',))


@local_command('//')
def _back_one_level(arguments):
    """
    Get back one level in prefixes (shortcut to 'using //')
    """
    if len(arguments) != 0:
        raise ExecutionError("You can't pass arguments to '//' command")
    
    return _using(('//',))


@local_command('login')
def _re_login(arguments):
    """
    Relogin to the server.
    """
    if len(arguments) != 0:
        raise ExecutionError("Login takes no arguments.")
    
    user_name = raw_input('User: ')
    password = getpass.getpass()
    
    #CommandExecuter is a singleton class, so doing login will affect the whole
    #program.
    import service_manager
    executer = service_manager.CommandExecuter()
    executer.login(user_name, password)

    #If an exception raise during the login, we won't reach this line.
    return 'Login done successfully.'


@local_command('help')
def _help(arguments):
    """
    Prints a help message about a command.
    Type 'help' without any parameter to get a general help.
    """
    if len(arguments) == 0:
        #Returning the general help.
        return """
   There are two kind of commands available: Internal commands
   and server-side commands.
   
   Internal commands are:
      {commands}
   
   For getting a list of server commands, type: command.list()

   For getting help about an specific internal command, type:
      help name_of_command

   For getting help about a server command, type:
      command.doc('command_name')
   
""".format(commands=LOCAL_COMMANDS.keys())
    
    #Returning help about a specific command.
    if arguments[0] in LOCAL_COMMANDS:
        return LOCAL_COMMANDS[arguments[0]].__doc__
    else:
        raise ExecutionError("Know nothing about `{0}'".format(arguments[0]))


@local_command('script')
def _script_command(arguments):
    """
    Execute a Python script inside the console.
    
    By invoking this command without any argument, an
    interactive shell will open and you can type your
    script directly in it. You can also pass a file name
    to this command, and it execute the script inside
    the given file.
    
    If you put one of Console's commands (Only server-side
    commands) between two dollar signs, it will be invoked
    in the right way.
    
    For example:
    >>> for i in range(3):
    >>>     $sample.show(i)$
    
    In the above example, 'sample.show' will be invoke
    like a Console's command.
    """
    if len(arguments) == 0:
        #Interactive mode.
        script_executer.execute_script_from_interactive_shell()
        return ' '
    
    if len(arguments) > 2:
        raise ExecutionError("'script' command takes at most one argument")
    
    script_executer.execute_script_file(arguments[0])
    
    #The script itself is responsible for printing out its results, so
    #we return an empty result here.
    return ' '

@local_command('watch')
def _watch_command(arguments):
    """
    this command can be used for executing a server command
    periodically.
    Example:
       watch 3 batch.status('IS_EOY_BRN')
    
    The first argument is in seconds, and represents how
    often the command should be executed. The second argument
    is the command to execute.
    """
    if len(arguments) < 2:
        raise ExecutionError('watch takes exactly two arguments.')
    
    try:
        period = float(arguments[0])
        #The 'local_command_parser' assumes that argumets separates by empty
        #spaces. But this command is an exception. So we have to append all of
        #the arguments to make the command string.
        command_string = ''
        for arg in arguments[1:]:
            command_string += arg
    except ValueError:
        raise ExecutionError("Invalid arguments")
    
    import service_manager
    import output_handler
    executer = service_manager.CommandExecuter()
    
    while True:
        try:
            output_handler.output_printer(
                                executer.execute_command(command_string))
            output_handler.print_horizonal_line()
            time.sleep(period)
        except Exception, error:
            raise ExecutionError(error)
        except KeyboardInterrupt:
            return

@local_command(('exit', 'quit'))
def _quit(arguments):
    """
    Terminates the program.
    """
    raise EOFError()


if os.name == 'posix':
    @local_command('!')
    def _execute_shell_command(arguments):
        """
        Execute a shell command from inside the
        delta console.
        Note that there have to be at least one
        space between `!' and the command.
        
        For example:
            > ! ps axjf | grep python
        """
        if len(arguments) < 1:
            raise ExecutionError('You have to specify a command to execute.')
        
        shell_command = ''
        for arg in arguments:
            shell_command += ' ' + arg

        os.system(shell_command)


#=======================SETTINGS HANDLERERS=========================

@setting_handler('timing')
def _set_timing(arguments):
    """Set the timing on or off.
    
    @param variable: Should be a tuple with one variable.
    """
    if len(arguments) != 1:
        raise ExecutionError("'set timing' takes exactly one argumnet.")
    
    if arguments[0].upper() in ('ON', 'TRUE', '1'):
        enable_timing = True
    elif arguments[0].upper() in ('OFF', 'FALSE', '0'):
        enable_timing = False
    else:
        raise ExecutionError('Inavlid argument {0}'.format(arguments[0]))
    
    utils.SETTINGS_DICT['timing'] = enable_timing
    
    return 'Timing is set to {0}'.format(enable_timing)

@setting_handler('debugging')
def _set_debugging(arguments):
    """
    Sets the debugging mode on pr off.

    @param arguments: Should be a tuple with one variable.

    @raise ExecutionError:  Execution error
    """

    if len(arguments) != 1:
        raise ExecutionError("'set debugging' takes exactly one argumnet.")

    if arguments[0].upper() in ('ON', 'TRUE', '1'):
        enable_debugging = True
    elif arguments[0].upper() in ('OFF', 'FALSE', '0'):
        enable_debugging = False
    else:
        raise ExecutionError('Inavlid argument {0}'.format(arguments[0]))

    utils.SETTINGS_DICT['debugging'] = enable_debugging

    return 'Debugging is set to {0}'.format(enable_debugging)

#===================================================================



def Execute(command, arguments):
    """Execute the given command locally.
    
    @param command: Command as a string.
    @param arguments: Arguments of the command as a tuple.
    """
    if LOCAL_COMMANDS.has_key(command):
        return LOCAL_COMMANDS[command](arguments)
    else:
        raise ExecutionError("Don't know how to execute {0}".format(command))

