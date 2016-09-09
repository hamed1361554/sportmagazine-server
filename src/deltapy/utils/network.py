'''
Created on May 29, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import struct

def ip_to_int(ip_address_str):
    '''
    Converts IP address to int.
    
    @param ip_address_str: ip address as str
    
    @return: int
    '''
    
    parts = ip_address_str.split('.')
    int_ip, = struct.unpack('i', struct.pack('BBBB', *map(int, parts)))
    return int_ip
    
def int_to_ip(int_ip):
    '''
    Converts IP address to int.
    
    @param ip_address_str: ip address as str
    
    @return: int
    '''
    
    result = '{0}.{1}.{2}.{3}'.format(*struct.unpack('BBBB', struct.pack('i', int_ip)))
    return result


