'''
Created on Feb 2, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.security.channel.authorizer.authorizer import ChannelAuthorizer
from deltapy.security.channel.authorizer import APP_CHANNEL_AUTHORIZER
from deltapy.application.decorators import register

@register(APP_CHANNEL_AUTHORIZER)
class ChannelAuthorizerComponent(ChannelAuthorizer):
    pass