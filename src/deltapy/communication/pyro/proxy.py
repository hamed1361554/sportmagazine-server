'''
Created on Sep 28, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''
import Pyro
import Pyro.core
from deltapy.communication.proxy import Proxy
from deltapy.communication.pyro.listener import PyroExceptionManager


class PyroProxy(Proxy):
    def __init__(self, ticket, user_name, host, port, service_name):
        Proxy.__init__(self, ticket, user_name)
        Pyro.config.PYRO_MULTITHREADED = 1
        Pyro.core.initClient()
        if service_name is None:
            service_name = 'pyro'
        pyro_url = 'PYROLOC://%s:%d/%s' % (host, port, service_name)
        self._server_proxy = Pyro.core.getProxyForURI(pyro_url)
        self._exception_manager = PyroExceptionManager()
        
    def open(self, user_name, password, **kwargs):
        try:
            self.ticket = self._server_proxy.login(user_name, password, **kwargs)
            self.user_name = user_name
        except Exception as ex:
            self._exception_manager.to_internal(ex)

    def execute_ex(self, request, **options):
        try:
            return self._server_proxy.execute_ex(request, **options)
        except Exception as ex:
            self._exception_manager.to_internal(ex)

    def execute_by_user(self, ticket, user_name, command_key , *args, **kargs):
        try:
            return self._server_proxy.execute(ticket,
                                              user_name,
                                              command_key,
                                              *args,
                                              **kargs)
        except Exception as ex:
            self._exception_manager.to_internal(ex)
        
    def close(self):
        try:
            self._server_proxy.logout(self.ticket, self.user_name)
        except Exception as ex:
            self._exception_manager.to_internal(ex)
