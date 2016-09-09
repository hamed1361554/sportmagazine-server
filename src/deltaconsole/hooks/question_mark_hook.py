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
Created on Feb 8, 2011
@author: Aidin Gharibnavaz

Hook to handle question mark at the end of the command,
(Getting document of that command.)
'''
from service_manager import CommandExecuter


def handle_question_mark(raw_command_string):
    """If there's a question mark at the end of the
    command, it adds a `command.doc' to it.
    """
    raw_command_string = raw_command_string.strip()

    if not raw_command_string.endswith('?'):
        return

    raw_command_string = raw_command_string[:-1] #Removes question mark
    raw_command_string = 'command.doc("{0}")'.format(raw_command_string.strip())
    
    return raw_command_string

#========== Registering the Hook ==========
executer = CommandExecuter()
executer.register_before_execution_hook(handle_question_mark)

