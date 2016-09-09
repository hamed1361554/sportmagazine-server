'''
Created on Sep 17, 2014

@author: Abi.Mohammadi
'''

import zmq

from deltapy.communication.proxy import Proxy

def make_message(command, data):
    return yaml.dump(dict(command=command, data=data))

class ZmqProxy(Proxy):
    def __init__(self, ticket, user_name, host, port, service_name):
        Proxy.__init__(self, ticket, user_name)

        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect('tcp://{0}:{1}'.format(host, port))
        
    def open(self, user_name, password, **kwargs):
        self._socket.send(make_message('login', dict(user_name=user_name, password=password, options=kwargs)))
        response = self._socket.recv()
        login_data = yaml.load(response) 
        self.ticket = login_data['ticket']
        self.user_name = user_name

    def execute_ex(self, request, **options):
        self._socket.send(make_message('execute', request))
        response = yaml.load(self._socket.recv())
        return response 

    def execute_by_user(self, ticket, user_name, command_key , *args, **kargs):
        raise NotImplementedError()
        
    def close(self):
        self._socket.send(make_message('logout', dict(user_name=self.user_name, ticket=self.ticket)))
        self._socket.close()
        self._context.shutdown()
