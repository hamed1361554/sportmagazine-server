'''
Created on Nov 23, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.application.services as application

@command('app.name')
def get_name():
    '''
    Returns application name.
    @return: str
    '''
    return application.get_name()

@command('app.enlist')
def enlist_app(app_name, 
               instance_name, 
               user_name, 
               ticket, 
               listener_params):
    '''
    Enlists an application.
    
    @param app_name: application name
    @param instance_name: application instance name
    @param user_name: user name
    @param ticket: ticket of the user
    @param listener_params: parameters of the listener
    '''

    return application.enlist_app(app_name, 
                                  instance_name, 
                                  user_name, 
                                  ticket, 
                                  listener_params)

@command('app.introduce')
def introduce():
    '''
    Introduces the application.
    '''               
    return application.introduce()