# Copyright (c) 2000 - 2010 Majid Vesal <mva_vesal@yahoo.com> and
# Abi M.Sangarab <abisxir@gmail.com>
#
# This file is part of Deltapy.

# Deltapy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# Deltapy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Deltapy. If not, see <http://www.gnu.org/licenses/>.
'''
Created on Aug 12, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
import optparse
import sys 

from deltapy.core import DeltaObject
from deltapy.utils import get_module_dir, activator

class CommandLineAction(DeltaObject):
    '''
    '''
    
    def __init__(self, name, short_option, long_option, help):
        DeltaObject.__init__(self)
        self.parser = optparse.OptionParser()
        self.short_option = short_option
        self.long_option = long_option
        self.help = help
        self._set_name_(name)
    
    def execute(self):
        '''
        Executes command line action.
        '''
        
        raise NotImplementedError()
    
    def __str__(self):
        return '[{name}]'.format(name = self.get_name())

class AdminManager(DeltaObject):
    '''
    '''
    
    def __init__(self):
        '''
        '''
        
        DeltaObject.__init__(self)
        
        self._actions = {}
        self._parser = optparse.OptionParser()
        self._load_()
    
    def _load_(self):
        '''
        Loads all command line actions.
        '''

        action_modules = {}
        file_path = os.path.join(get_module_dir(__name__), 'actions')
        for file_name in os.listdir(file_path):
            file_full_path = os.path.join(file_path, file_name)
            if file_full_path.endswith('.py') or file_full_path.endswith('.pyc'):
                module_name = file_name.split('.')[0]
                action_modules['deltapy.admin.actions.{module}'.format(module = module_name)] = file_full_path
        
        for module_name in action_modules:
            types = activator.get_types(module_name, CommandLineAction, parent = 'deltapy.admin.actions')
            for command_line_action_class in types:
                action = command_line_action_class()
                self._actions[action.get_name()] = action
                
    def _print_usage_(self):
        '''
        Prints usage message.
        '''
        
        print "Usage: deltapy-admin [options]"
        print ""
        print "type -h or --help for more information"

    def _print_help_(self):
        '''
        Prints help message.
        '''
        
        print "Usage: deltapy-admin [options]"
        print ""
        print "Options:"
        print "{short_option}, {long_option}\t\t\t{help}".format(short_option = '-h', 
                                                                 long_option = '--help',
                                                                 help = 'show this help message and exit')
        for action in self._actions.values():
            print "{short_option}, {long_option}\t\t\t{help}".format(short_option = action.short_option, 
                                                                     long_option = action.long_option, 
                                                                     help = action.help)
        
    def process(self):
        '''
        Processes command line actions.
        '''
        
        if len(sys.argv) == 1:
            self._print_usage_()
            sys.exit(0)
            
        if '-h' in sys.argv or '--help' in sys.argv:
            if len(sys.argv) == 2:
                self._print_help_()
                sys.exit(0)
            else:
                action_name = sys.argv[2]
                if action_name not in self._actions:
                    print 'Command [%s] not found.' % action_name
                    print 'Type deltapy-admin --help for more information.'
                    sys.exit(0)
                else:
                    action = self._actions[action_name]
                    action.parser.print_help()
                    sys.exit(0)
                    
        for option in sys.argv:
            for action in self._actions.values():
                if option in [action.short_option, action.long_option]:
                    action.execute()
                    
#        options, args = self._parser.parse_args()
#        for action in self._actions.values():
#            if hasattr(options, action.get_name()):
#                if getattr(options, action.get_name()) is not None:
#                    action.execute(options, args)
