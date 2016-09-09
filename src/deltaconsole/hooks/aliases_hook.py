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

Hooks to handle aliases.
'''

import sys
import os
from ConfigParser import SafeConfigParser
from service_manager import CommandExecuter
from decorators import local_command

#==================== CONFIGURING ALIASES FILE ====================
#Keeps all of the aliases.
ALIASES = []

if os.name == 'nt':
    __ALIAS_CONFIG_FILE = os.path.join(
                              os.path.abspath(
                                  os.path.dirname(
                                      sys.modules[__name__].__file__)),
                              'alias.conf')
else:
    __ALIAS_CONFIG_FILE = '/etc/deltaconsole/alias.conf'


#Loading aliases at the import time.
__ALIAS_CONFIGS = SafeConfigParser()
#Making config parser case-sensitive.
setattr(__ALIAS_CONFIGS, 'optionxform', str)

if len(__ALIAS_CONFIGS.read(__ALIAS_CONFIG_FILE)) <= 0:
    print "WARNING: could not read `alias.conf' file, or file is empty."
    ALIASES = []
else:
    if __ALIAS_CONFIGS.has_section('ALIASES'):
        ALIASES = __ALIAS_CONFIGS.items('ALIASES')


#=================== DEFINING HOOKS =====================

def replace_aliases(command_string):
    """Replace aliases in the given command string
    with their equivalents and returns the result.
    
    @param command_arguments_string: Raw entered command
        as string.
    
    @return: Command string which its aliases is
        replaced.
    """
    result = command_string

    if len(ALIASES) <= 0:
        return result
    
    #To find out whether we walk through all of the string, we use `done'
    #variable. If during one loop over aliases we don't find any of them
    #inside the string, `done' became True, otherwise, it is False.
    while True:
        done = True
        for alias in ALIASES:
            alias_index = result.find(alias[0])
            if alias_index == 0:
                #The command itself is alias.
                end_index = result.find('(')
                if end_index <= 0:
                    raise Exception("Invalid command string.")
                result = __make_real_command(result, alias)
                done = False
                #Breaking the `for' loop, to start searching for aliases again.
                break
            elif alias_index > 0:
                if result[alias_index+len(alias[0])] != '(':
                    end_index = alias_index + len(alias[0]) - 1
                else:
                    end_index = result.find(')', alias_index)
                
                if end_index < 0:
                    raise Exception("Invalid command string.")

                real_command =  __make_real_command(result[alias_index:end_index+1],
                                                    alias)
                result = result[:alias_index] + real_command + \
                         result[end_index+1:]
                done = False

        if done:
            break

    return result

def __make_real_command(arg_string, alias):
    """Make real command from the given string, by
    replacing aliases and their arguments in it.
    
    @param arg_string: String to replace aliases in it.
    @param alias: The alias as in the aliases.conf file.
    
    @return: Real command.
    """
    alias_command, ignore_me, alias_args = arg_string.partition('(')

    if len(alias_args) <= 1:
        #No arguments specified
        return alias[1]
    
    #Removing last ')'
    if alias_args.endswith(')'):
        alias_args = alias_args[:len(alias_args)-1]

    arg_iterator = 0
    result = alias[1]
    for arg in alias_args.split(','):
        if '#{0}'.format(arg_iterator) not in result:
            raise Exception("Alias of `{0}' dose not have "
                            "argument #{1}".format(alias[0], arg_iterator))

        result = result.replace('#{0}'.format(arg_iterator), arg)
        #result = result[:arg_index] + arg + result[arg_index+1:]
        arg_iterator += 1

    return result


#========== REGISTERING HOOKS ==========
executer = CommandExecuter()
executer.register_before_execution_hook(replace_aliases)


#========== ADDING SOME LOCAL COMMANDS ==========

class ExecutionError(Exception):
    pass

@local_command('aliases')
def _aliases(arguments):
    '''
    If uses without any arguments, it print out list of
    available aliases.
    If you specify an alias as its first argument, it
    prints the alias command.
    
    You can set aliases in `alias.conf' file.
    '''
    if len(arguments) <=0:
        #Printing aliases.
        result = 'Aliases are:\n   '
        for alias in ALIASES:
            result += alias[0] + ', '
        return result
    elif len(arguments) > 1:
        raise ExecutionError("`aliases' command accepts zero or one argument.")
    else:
        for alias in ALIASES:
            if alias[0] == arguments[0]:
                return alias[1]
        
        raise ExecutionError("Alias `{0}' not found.".format(arguments[0]))
