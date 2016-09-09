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
Created on Dec 14, 2009
@author: Aidin Gharibnavaz

This module contains decorators used in the project.
'''

import local_executer


def local_command(command_name):
    """Using this decorator, a function can be registred as
    a local command. Simply put this above your function,
    and give your command a name.
    
    @param command_name: Name of the command (The command user type in the
                         console). Also can be a tuple of more that one name.
    """
    def wrap(command_function):
        if isinstance(command_name, basestring):
            local_executer.LOCAL_COMMANDS[command_name] = command_function
        elif isinstance(command_name, tuple):
            for name in command_name:
                local_executer.LOCAL_COMMANDS[name] = command_function
        else:
            raise Exception('Invalid use of "local_command" decorator')
        
        #We don't really want to decorate this function.
        return command_function
    
    return wrap


def setting_handler(setting_name):
    """Using this decorator, a function can be registred as
    a setting handler. Simply put this above your function,
    and pass the name of the setting to it.
    
    @param command_name: Name of the setting.
    """
    def wrap(command_function):
        if isinstance(setting_name, basestring):
            local_executer.SETTING_FUNCTIONS[setting_name] = command_function
        elif isinstance(setting_name, tuple):
            for name in setting_name:
                local_executer.SETTING_FUNCTIONS[name] = command_function
        else:
            raise Exception('Invalid use of "local_command" decorator')
        
        #We don't really want to decorate this function.
        return command_function
    
    return wrap

