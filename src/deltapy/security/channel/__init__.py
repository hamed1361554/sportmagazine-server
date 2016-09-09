'''
Created on Jan 30, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.packaging.package import Package

APP_SECURITY_CHANNEL = 'security.channel'

class ChannelPackage(Package):
    
    __depends__ = ['deltapy.security.authentication',
                   'deltapy.event_system',]
    
    __disable__ = False