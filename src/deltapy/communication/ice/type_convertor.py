'''
Created on Nov 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.type_convertor import TypeConvertor
import deltapy.config.services as config

class IceTypeConvertor(TypeConvertor):
    '''
    Ice type convertor.
    '''
    
    def __init__(self):
        TypeConvertor.__init__(self)
        import deltapy.communication.ice.utils as ice_utils
        
        ice_utils.set_encodings(config.get_app_config_store().get('global', 
                                                                  'encoding', 
                                                                  'utf-8'), 
                                'utf-8')
    
    def to_internal(self, obj):
        '''
        Converts an extranal object type to internal type.
        
        @param obj: external object
        @return: object
        '''
        import deltapy.communication.ice.utils as ice_utils
        return ice_utils.dobject_to_object(obj)
    
    def to_external(self, obj):
        '''
        Converts an internal object type to external object type.
        
        @param obj: internal object
        @return: object
        '''
        import deltapy.communication.ice.utils as ice_utils
        return ice_utils.object_to_dobject(obj)
    
    