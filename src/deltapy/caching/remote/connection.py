'''
Created on Jan 26, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.core import DeltaObject
import socket
import cPickle

MAX_DATA_SIZE = 1024*1024

class RemoteCacheConnection(DeltaObject):
    '''
    Cache connection class.
    '''
    def __init__(self, ip, port, auth_key):
        '''        
        @param ip:
        @param port:
        @param auth_key:
        '''
        
        self._ip = ip
        self._port = port
        self._auth_key = auth_key
        self._socket = self._login()
        
    def _login(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.connect((self._ip, self._port))
        return sock 

    
    def execute(self, command, *data):
        request = (command, data)
        request= cPickle.dumps(request)
        self._socket.send(request)
        response = self._socket.recv(MAX_DATA_SIZE)
        if response is not None:
            response = cPickle.loads(response)
            if issubclass(response.__class__, Exception):
                raise response
        return response
