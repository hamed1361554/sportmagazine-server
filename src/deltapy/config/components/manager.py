'''
Created on Jan 31, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.config.manager import ConfigManager
from deltapy.application.decorators import register
from deltapy.locals import APP_CONFIG

import deltapy.application.services as application_services

@register(APP_CONFIG)
class ConfigManagerComponent(ConfigManager):
    '''
    
    '''
    
    def __init__(self):
        
        ConfigManager.__init__(self,
                               application_services.get_default_settings_folder_name(), 
                               application_services.get_options())
        
        self.load_all_configs(application_services.get_name())