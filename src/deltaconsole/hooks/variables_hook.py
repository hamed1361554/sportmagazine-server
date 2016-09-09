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
Created on Feb, 2011
@author: Aidin Gharibnavaz

Hooks to handle runtime variables.
'''
import re

from service_manager import CommandExecuter
from decorators import local_command


#=================== DEFINING HOOKS =====================

def remove_variable_from_command(raw_command_string):
    """This will call before the execution of the command,
    to remove the variable from the command string. (The
    variable that appears at the left-side of the command)
    @see:fill_variable to find out how we fill the variable
    later.
    """
    variable, command_string = __split_variable(raw_command_string)
    return command_string

def fill_variable(raw_command, executed_command, execution_result):
    """Fills the execution result in the variable.
    It parses the `raw_command' and extract the variable name,
    then puts the `execution_result' in it.
    """
    variable_name, command_string = __split_variable(raw_command)
    if variable_name is None:
        return
    
    USER_VARIABLES[variable_name] = execution_result

def __split_variable(raw_command_string):
    """See whether user specified a variable in her/his
    command. If she/he dose, it extract the variable
    form the raw_command_string, and returns them. Else,
    it returns the original command.
    
    @param raw_command_string: The inputed command without
        modification.
    @return: Tuple: (variable, command)
        If user did not specify a variable, the first
        element is None.
    """
    command_string = raw_command_string.strip()
    
    splited_command = command_string.split('=', 1)
    
    if len(splited_command) <= 1:
        return (None, raw_command_string)
    
    variable, command = splited_command
    variable = variable.strip()
    command = command.strip()
    
    if variable.find(' ') != -1 or variable.find('(') != -1:
        return (None, raw_command_string)
    
    return (variable, command)

def replace_varibales_in_the_command(command_string):
    """Replaces variables in the command string, with
    self.USER_VARIABLES['var_name'] string, which can be
    evaluated to get the value of the variable.
    """
    variables = re.findall('\$[a-zA-Z0-9_]*', command_string)

    if len(variables) <= 0:
        return command_string

    for var in variables:
        if var[1:] not in USER_VARIABLES:
            raise Exception("Unknown variable `{var_name}'".format(
                                                             var_name=var[1:]))

        var_value = "self.USER_VARIABLES['{var_name}']".format(var_name=var[1:])
        command_string = command_string.replace(var, var_value)
    return command_string


#========== REGISTERING HOOKS ==========

executer = CommandExecuter()
executer.register_before_execution_hook(remove_variable_from_command)
executer.register_before_execution_hook(replace_varibales_in_the_command)

executer.register_after_execution_hook(fill_variable)
#Putting variables in the executer class, so they will available at
#the time of evaluating the command.
setattr(executer, 'USER_VARIABLES', {})
USER_VARIABLES = executer.USER_VARIABLES


#========== ADDING SOME LOCAL COMMANDS ==========

class ExecutionError(Exception):
    pass

@local_command('variables')
def _available_variables(arguments):
    '''
    Prints all of the available variables.
    
    To assign a value to a variable, type:
        var = server_command(...)
    Then you can use it like this:
        print $var
        server_command($var, ...)
    '''
    if len(arguments) > 0:
        raise ExecutionError("`variables' takes no arguments.")
    
    if len(USER_VARIABLES) <= 0:
        return " No variable registered yet."
    
    result = [{'name':name, 'type':type(value)}
              for name, value in USER_VARIABLES.iteritems()]
    return result

@local_command('print')
def _print(arguments):
    '''
    Prints the expression in front of it.
    
    For example:
       print $var
       print len($var)
       print $var['key']
       print 3 * $var
    
    `$var' is a variable. For more info, see the
    help of the `variables' command.
    '''
    to_print = ' '
    to_print = to_print.join(arguments)
    
    if len(to_print) <= 0:
        return ' '

    try:
        to_print = to_print.replace('self.', '')
        return eval(to_print)
    except Exception as error:
        raise ExecutionError('{type}: {error}'.format(type=
                                                      error.__class__.__name__,
                                                      error=error))
