'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.channel.authenticator.authenticator import ChannelAuthenicator
from deltapy.application.decorators import register
from deltapy.security.channel.authenticator import APP_SECURITY_CHANNEL_AUTHENTICATOR

@register(APP_SECURITY_CHANNEL_AUTHENTICATOR)
class ChannelAuthenicatorComponent(ChannelAuthenicator):
    pass