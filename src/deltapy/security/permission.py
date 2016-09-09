'''
Created on May 22, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject
import deltapy.security.services.permission_holder as permission_holder_services 

class BasePermission(DeltaObject):
    '''
    '''
    
    def __init__(self):
        DeltaObject.__init__(self)
        
        permission_holder_services.hold(self)
    
    def update(self, **options):
        '''
        Updates permission.
        '''
        
        raise NotImplementedError()
    
    def __hash__(self):
        raise NotImplementedError('You must implement __hash__ method for your permission class.')
    
    def __str__(self):
        raise NotImplementedError('You must implement __str__ method for your permission class.')
    
