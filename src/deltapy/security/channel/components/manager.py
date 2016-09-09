'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.channel.manager import ChannelManager
from deltapy.application.decorators import register
from deltapy.security.channel import APP_SECURITY_CHANNEL

@register(APP_SECURITY_CHANNEL)
class ChannelManagerComponent(ChannelManager):
    def __init__(self):
        ChannelManager.__init__(self)
        
        self.load()
        
    