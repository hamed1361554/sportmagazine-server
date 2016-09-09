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
"""This module is responsible for handling the prompt.
"""

import service_manager
from utils import SETTINGS_DICT

APP_NAME = None

def get_prompt_string():
    """Return prompt that should appears in the console's command
    line. (i.e 'corebanking>')
    
    @return: A string.
    """
    global APP_NAME
    if APP_NAME is None:
        #Try getting application name.
        APP_NAME = __get_app_name()
    
    prompt = SETTINGS_DICT['command_prefix']
#    if prompt.endswith('.'):
#        prompt = prompt[:len(prompt)-1]
    if prompt:
        prompt = prompt.replace('.', '/')
    
    return '{0}/{1}> '.format(APP_NAME, prompt)

def __get_app_name():
    """Try to get application name, that we're connected to.
    If it couldn't get the name, it returns empty string.
    """
    executer = service_manager.CommandExecuter()
    try:
        app_info = executer.execute_command('app.introduce()')
        return app_info['name']
    except Exception:
        #In case of any error, return empty string.
        return ''
