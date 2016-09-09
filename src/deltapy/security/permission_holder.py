'''
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DeltaException

class PermissionHolderException(DeltaException):
    '''
    '''

class PermissionDuplicatedException(DeltaException):
    '''
    '''

class PermissionHolder(DeltaObject):
    '''
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        
        self._holder = {}
    
    def hold(self, permission):
        '''
        Holds the permission.
        
        @param permission: permission instance
        '''
        
        if permission in self._holder:
            message = _('Permission [{permission_id}] already exists.')
            raise PermissionDuplicatedException(message.format(permission_id = str(permission)))
        self._holder[permission] = permission
        
    def get_permissions(self):
        '''
        Returns all permissions in holder.
        
        @return: [Permission]
        '''
        
        return self._holder.values()
    
    def sync(self, **options):
        '''
        Synchronizes permissions with database.

        @param **options:
           options to pass along with this command.
        '''
        for permission in self.get_permissions():
            permission.update(**options)
        
