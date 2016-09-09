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
Created on Aug 15, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import os
import sys

from deltapy.admin.manager import CommandLineAction
from deltapy.core import DeltaException
from deltapy.utils import activator
from deltapy.application.base import Application

class ApplicationServeException(DeltaException):
    '''
    '''

class ApplicationServeAction(CommandLineAction):
    '''
    '''
    
    def __init__(self):
        CommandLineAction.__init__(self, 'serve', '-s', '--serve', 'serves the deltapy application')
        
        self.parser.add_option('-s', '--serve', metavar = 'APPLICATION_NAME', dest = 'app_name', help = 'serves the deltapy application')

    def execute(self):
        '''
        Executes command line action.
        '''

        options,args = self.parser.parse_args()
        if options.app_name is None or len(options.app_name) == 0:
            raise ApplicationServeException('You must specify application name to serve.')
        if not os.path.exists(os.path.join('.', options.app_name)):
            raise ApplicationServeException('Application directory [{app_name}] not found.'.format(app_name = options.app_name))
        
        app_classes = activator.get_types(options.app_name, Application)
        if len(app_classes) == 0:
            raise ApplicationServeException('There is not any deltapy application to serve..')
        
        app_instance = app_classes[0]()
        app_instance.run()
        
