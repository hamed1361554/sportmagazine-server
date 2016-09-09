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
Created on Feb 4, 2010
@author: Aidin Gharibnavaz

This module is responsible for handling the
GNU readline features, such as console's history,
auto complete, etc.
'''
import os
import service_manager
from utils import ANSICOLORS, SETTINGS_DICT

class ReadlineHandler(object):
    '''
    This class can be use as a completer for the
    readline module.
    '''
    def __init__(self):
        '''
        Initializing the class by getting command list
        from the server.
        '''
        self.__match_list = None
        
        #Setting readline properties
        readline.set_history_length(50)
        
        history_file = os.path.join(os.environ["HOME"], ".dschistory")
        #Try to read history file.
        if os.path.exists(history_file):
            readline.read_history_file(history_file)
        #Saving history at exit.
        atexit.register(readline.write_history_file, history_file)
        
        #Setting up the completer.
        try:
            executer = service_manager.CommandExecuter()
            self.__commands_list = executer.execute_command('command.list()')
            #Setting the compelter.
            readline.set_completer(self.completer)
            readline.parse_and_bind('tab: complete')
        except Exception:
            #We couldn't get the command's list. So remove the completer
            #methods from the readline.
            readline.set_completer()
    
    def completer(self, text, status):
        '''
        The completer method.
        It returns the commands that match the 'text'.
        '''
        if status == 0:
            #This is the first time that readline calls this method.
            #Creating the matching list.
            user_inputed_text = text
            prefix = SETTINGS_DICT['command_prefix']
            if prefix:
                user_inputed_text = prefix + text
                user_inputed_text = user_inputed_text.replace('/', '.')
                self.__match_list = [x.replace(prefix, '')
                                     for x in self.__commands_list
                                     if x.startswith(user_inputed_text)]
            else:
                self.__match_list = [x for x in self.__commands_list
                                     if x.startswith(user_inputed_text)]
        
        try:
            return self.__match_list[status]
        except IndexError:
            return None


#Setting up readline, if it's available.
try:
    import readline
    import atexit
    
    ReadlineHandler()
except ImportError:
    pass

