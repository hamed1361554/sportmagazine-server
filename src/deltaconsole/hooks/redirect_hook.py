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

A hook that adds `redirect to a file' feature.
'''
from service_manager import CommandExecuter

def remove_filename_from_command(raw_command_string):
    """Removes everything after '>' sign."""
    index = raw_command_string.find('>')
    if index > 0:
        raw_command_string = raw_command_string[:index]
    
    return raw_command_string

def write_result_in_file(raw_command, executed_command, result):
    """Write the result in the file that specified
    after '>'.
    """
    filename = _extract_filename(raw_command)
    
    if filename is None:
        return
    
    with open(filename, 'a') as outputfile:
        outputfile.write('{0}'.format(result))
        outputfile.write('\n')


def _extract_filename(command_string):
    """Extract the file name to redirect to (the string
    after '>') and returns it.
    It returns None if there's nothing after '>', or
    no redirection specified.
    """
    command, greater_char, filename = command_string.partition('>')
    
    if filename in ('', None) or filename.isspace():
        return None
    
    return filename.strip()

#========== Registering Hooks ==========
executer = CommandExecuter()
executer.register_before_execution_hook(remove_filename_from_command)
executer.register_after_execution_hook(write_result_in_file)

