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

A hook for sorting the output.
'''

from service_manager import CommandExecuter
from decorators import setting_handler

ENABLED = False

class ExecutionError(Exception):
    pass


def sort(raw_command, executed_command, result):
    """Sort the result, if it's a list."""
    if ENABLED:
        if isinstance(result, list):
            return sorted(result)

#***** REGISTERING HOOKS *****
executer = CommandExecuter()
executer.register_after_execution_hook(sort)

#***** SETTING COMMAND *****
@setting_handler('sorting')
def _set_timing(arguments):
    if len(arguments) != 1:
        raise ExecutionError("'set timing' takes exactly one argumnet.")

    global ENABLED
    if arguments[0].upper() in ('ON', 'TRUE', '1'):
        ENABLED = True
    elif arguments[0].upper() in ('OFF', 'FALSE', '0'):
        ENABLED = False
    else:
        raise ExecutionError('Inavlid argument {0}'.format(arguments[0]))

    return 'Sorting is set to {0}'.format(ENABLED)
