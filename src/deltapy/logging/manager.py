'''
Created on Aug 11, 2009

@author: mohammadi, vesal
'''

import logging
import logging.config

class LoggingManager:
    '''
    For managing logs
    '''
    def __init__(self, config_file):
        '''
        The constructor.
        
        @param configFile: the full name of logging configuration file
        '''
        self._config_file = config_file
        self.reload_configs()
    
    def get_logger(self, **kargs):
        '''
        Returns the associated logger.
        
        @param name: name of the logger
        @param others: other replacement logger names
        '''
        name = kargs.get('name', None)
        others = []
        if kargs.has_key('others'):
            others = kargs['others']
        if len(others):
            for logger in [name] + others:
                if logger in logging.Logger.manager.loggerDict:
                    return logging.getLogger(logger)
        return logging.getLogger(name)
    
    def reload_configs(self):
        '''
        Re-reads configs from the config file.
        '''
        logging.config.fileConfig(self._config_file)
    
    def debug(self, msg, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):    
        logging.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        logging.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        logging.critical(msg, *args, **kwargs)
        
    def info(self, msg, *args, **kwargs):    
        logging.info(msg, *args, **kwargs)

