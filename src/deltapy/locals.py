'''
Created on Aug 4, 2009

@author: abi m.s, majid v.a
'''

__app__ = None

def _set_app_(app):
    '''
    Sets the current application.
    
    @param app: application instance
    '''
    global __app__
    __app__ = app

def get_app():
    '''
    Returns current application instance.
    
    @return: Application
    '''
    global __app__
    return __app__

def get_app_context():
    '''
    Returns application context.
    
    @return: ApplicationContext
    '''
    
    return get_app().context

APP_COMMUNICATOR = "communicator"
APP_SECURITY = "security"
APP_LOGGING = "logging"
APP_CACHING = "caching"
APP_CONFIG = "config"
APP_DATABASE = "database"
APP_COMMANDER = "commander"
APP_PACKAGING = "packaging"
APP_SCHEDULING = "scheduling"
APP_SCRIPTING = "scripting"
APP_TRANSACTION = "transaction"
APP_BATCH = "batch"