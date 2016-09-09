'''
Created on Dec 24, 2012

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.application.decorators import register
from deltapy.communication.ice.json import ICE_JSON_FACTORY
from deltapy.communication.ice.json.factory import IceJsonFactory
from deltapy.communication.services import register_factory

@register(ICE_JSON_FACTORY)
class IceJsonFactoryComponent(IceJsonFactory):
    def __init__(self):
        IceJsonFactory.__init__(self)
        
        register_factory('ice_json', IceJsonFactory())