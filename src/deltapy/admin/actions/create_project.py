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
import datetime

from deltapy.admin.manager import CommandLineAction
from deltapy.core import DeltaException
from deltapy.utils import get_module_dir

class CreateProjectException(DeltaException):
    '''
    '''

class CreateProjectAction(CommandLineAction):
    '''
    '''
    
    def __init__(self):
        CommandLineAction.__init__(self, 'create', '-c', '--create', 'creates a new deltapy application')
        
        self.parser.add_option('-c', '--create', metavar = 'APPLICATION_NAME', dest = 'app_name', help = 'creates a new deltapy application')
        self.parser.add_option('-l', '--log_path', metavar = 'LOG_PATH', dest = 'logging_path', help = 'determines application logging path')
        
    def _validate_application_name_(self, app_name):
        '''
        Validates application name.
        
        @param app_name: application name
        '''
        
    def _get_template_(self, name):
        '''
        
        @param name:
        '''
        
        templates_dir = os.path.join(get_module_dir('deltapy.admin.actions'), 'templates')
        file = open(os.path.join(templates_dir, name))
        return file.read()
    
    def _create_application_(self, app_name, **options):
        '''
        Creates application.
        
        @param app_name: application name
        @param **options:
        '''

        if app_name is None or len(app_name) == 0:
            raise CreateProjectException('You should specify application name by --create or -c parameter.')

        self._validate_application_name_(app_name)

        application_dir = os.path.join('.', app_name)
        application_module = os.path.join(application_dir, '__init__.py')
        
        os.mkdir(app_name)
        file = open(application_module, 'wb')
        
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        
        template = self._get_template_('application')
        application_class_name = \
            '{application_name}Application'.format(application_name = app_name.capitalize())
        file.write(template.format(application_class_name = application_class_name))
        file.close()
        
        settings_dir = os.path.join(app_name, 'settings') 
        os.mkdir(settings_dir)
        
        logging_path = options.get('logging_path')
        if logging_path is None:
            logging_path = os.path.join(application_dir, 'log')
        if not logging_path.endswith(os.path.sep):
            logging_path += os.path.sep
        
        if not os.path.exists(logging_path):
            os.mkdir(logging_path)
            
        file = open(os.path.join(settings_dir, 'logging.config'), 'wb')
        template = self._get_template_('settings/logging.config')
        file.write(template.format(logging_path = logging_path))
        file.close()

        file = open(os.path.join(settings_dir, 'app.config'), 'wb')
        template = self._get_template_('settings/app.config')
        file.write(template.format(app_name = app_name))
        file.close()
        
        file = open(os.path.join(settings_dir, 'communication.config'), 'wb')
        file.write(self._get_template_('settings/communication.config'))
        file.close()
        
        file = open(os.path.join(settings_dir, 'database.config'), 'wb')
        file.write(self._get_template_('settings/database.config'))
        file.close()

        file = open(os.path.join(settings_dir, 'caching.config'), 'wb')
        file.write(self._get_template_('settings/caching.config'))
        file.close()

        file = open(os.path.join(settings_dir, 'request_processor.config'), 'wb')
        file.write(self._get_template_('settings/request_processor.config'))
        file.close()

    def _create_package_(self, package_name, **options):
        '''
        Creates a new package.
        
        @param package_name: package name
        @param **options: 
        '''

        head, sep, package_pure_name = package_name.rpartition('.')
        
        package_dir = package_name.replace('.', os.path.sep)
        services_dir = os.path.join(package_dir, 'services')
        commands_dir = os.path.join(package_dir, 'commands')
        components_dir = os.path.join(package_dir, 'components')
        
        os.mkdir(package_dir)
        file = open(os.path.join(package_dir, '__init__.py'), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        
        template = self._get_template_('package')
        component_id = options.get('component_id')
        if component_id is None:
            component_id = \
                '{package_name}_COMPONENT_ID'.format(package_name = package_name.replace('.', '_').upper())
        component_id_str = \
            "{component_id} = '{package_name}'".format(component_id = component_id,
                                                       package_name = package_name)
        file.write(template.format(component_id = component_id_str,
                                   package_name = package_pure_name.capitalize()))
        
        file.close()
        
        class_name = options.get('class_name', package_pure_name.capitalize())
        component_file_name = options.get('class_file', 'main.py')
        if not component_file_name.endswith('.py'):
            component_file_name += '.py'
        file = open(os.path.join(package_dir, component_file_name), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        template = self._get_template_('class')
        file.write(template.format(class_name = class_name))
        file.close()

        os.mkdir(components_dir)
        file = open(os.path.join(components_dir, '__init__.py'), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        file.close()
        
        file = open(os.path.join(components_dir, component_file_name), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        template = self._get_template_('component')
        file.write(template.format(class_name = class_name,
                                   package_name = package_name,
                                   component_id = component_id,
                                   module = component_file_name.replace('.py', '')))
        file.close()

        os.mkdir(services_dir)
        file = open(os.path.join(services_dir, '__init__.py'), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        template = self._get_template_('service')
        file.write(template.format(package_name = package_name,
                                   component_id = component_id))
        file.close()

        os.mkdir(commands_dir)
        file = open(os.path.join(commands_dir, '__init__.py'), 'wb')
        template = self._get_template_('module')
        file.write(template.format(creation_date = datetime.date.today().strftime('%B %d %Y'),
                                   author = '<author>'))
        file.write(os.linesep)
        template = self._get_template_('command')
        file.write(template.format(package_name = package_name))
        file.close()
        
    def execute(self):
        '''
        Executes command line action.
        '''

        options,args = self.parser.parse_args()
        
        self._create_application_(options.app_name, 
                                  logging_path = options.logging_path)
        
        example_package_name = \
            '{app_name}.example'.format(app_name = options.app_name)
        self._create_package_(example_package_name)