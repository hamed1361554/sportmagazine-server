'''
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.security.services.permission_holder as permission_holder_services 

@command('security.permission.sync')
def sync(**options):
    '''
    Synchronizes permissions with database.

    @param **options:
       options to pass along with this command.
    '''
    
    return permission_holder_services.sync(**options)

