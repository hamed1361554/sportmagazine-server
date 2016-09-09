'''
Created on May 30, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.communicator import Communicator
from deltapy.application.decorators import register
from deltapy.locals import APP_COMMUNICATOR

@register(APP_COMMUNICATOR)
class CommunicatorComponent(Communicator):
    '''
    The communicator class which is for maintaining listeners.
    '''
