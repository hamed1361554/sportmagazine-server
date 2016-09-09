'''
Created on Dec 24, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.logging.manager import LoggingManager
from deltapy.application.decorators import register
from deltapy.locals import APP_LOGGING
import deltapy.config.services as config
import deltapy.application.services as application

@register(APP_LOGGING)
class LoggingManagerComponent(LoggingManager):
    '''
    Logging manager component.
    '''

    def __init__(self):
        config_store = config.get_app_config_store('logging')
        if not config_store:
            raise Exception('The application has not logging configuration file.')
        LoggingManager.__init__(self, config_store.get_file_name())
         
        