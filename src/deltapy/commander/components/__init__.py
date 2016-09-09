'''
Created on Oct 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.manager import CommandManager
from deltapy.application.decorators import register
import deltapy.locals
from deltapy.transaction.decorators import transactional

#@register(deltapy.locals.APP_COMMANDER)
class TransactionalCommandManagerComponet(CommandManager):
    '''
    This class only is used for registering CommandManager in deltapy.
    '''

    @transactional(auto_commit = True)
    def execute(self, key, *args, **kargs):
        return CommandManager.execute(self, key, *args, **kargs)


