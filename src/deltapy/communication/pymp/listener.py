'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.communication.listener import Listener
from deltapy.communication.listener import Dispatcher
import multiprocessing
from multiprocessing.managers import BaseManager
from deltapy.utils.uniqueid import get_uuid

class PympDispatcher(Dispatcher):
    def __init__(self, listener):
        Dispatcher.__init__(self, listener)
        
    def _get_client_ip_(self):
        return '127.0.0.1'

class PympListener(Listener):
    def __init__(self, communicator, name, params):
        Listener.__init__(self, communicator, name, params)
        self._auth_key = get_uuid()
        self._manager = BaseManager(address=(self.host, self.port), authkey=self._auth_key)
        self._server = self._manager.get_server()
        self._dispatcher = PympDispatcher(self)
        self._manager.register('dispatcher', callable=lambda:self._dispatcher) 
        
    def start(self):
        self._server.serve_forever()

    def stop(self, force):
        self._server.stop()
        
    def create_proxy(self, **kwargs):
        pass
