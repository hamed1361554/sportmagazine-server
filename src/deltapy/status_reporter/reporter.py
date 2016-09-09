'''
Created on Nov, 2013

@author: Nastaran & Aidin
'''
import os
import socket
import traceback

from deltapy.utils.concurrent import run_in_thread
from deltapy.logging.services import get_logger
import deltapy.application.services as application_services
import deltapy.packaging.services as package_services
import deltapy.request_processor.services as request_processor_services
import deltapy.security.session.services as session_services

class ServerStatusReporter(object):
    
    LOGGER = get_logger(name='status_reporter')
    
    def run(self):
        '''
        Starts the reporter.
        '''
        run_in_thread(self._listen)
    
    def _listen(self):
        '''
        Listens on a socket.
        '''
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # For re-using a time-wait socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind('/var/run/{0}/{1}.sid'.format(application_services.get_name(),
                                                         os.getpid()))
        server_socket.listen(1)
        
        while True:
            try:
                connection, address = server_socket.accept()
                status_string = self._get_status()
                # Since we don't care how much data has been send before an
                # error happends, we use `sendall' instead of `send'.
                connection.sendall(status_string)
            except Exception as error:
                ServerStatusReporter.LOGGER.error(str(error))
                ServerStatusReporter.LOGGER.error(traceback.format_exc())
            finally:
                connection.close()
    
    def _get_status(self):
        '''
        Gets status of the system.
        
        @return: status of system as a string.
        @rtype: str
        '''
        # Gathering server status.
        
        status_string = ''
        
        status_string += 'Instance Name: {0}\n'.format(application_services.get_full_name())
        
        # Application name and version
        app_introduction = application_services.introduce()
        if 'name' in app_introduction:
            status_string += 'Name: {0}\n'.format(app_introduction['name'])
        if 'version' in app_introduction:
            status_string += 'Version: {0}\n'.format(app_introduction['version'])
        
        # Packages status
        loaded_packages_count = len(package_services.get_loaded_packages())
        disabled_packages = package_services.get_disabled_packages()
        
        status_string += 'Packages: Loaded={0}, Disabled={1}\n'.format(loaded_packages_count,
                                                                       len(disabled_packages))
        if len(disabled_packages) > 0:
            status_string += 'Disabled Packages: [{0}'.format(disabled_packages[0])
            for disabled_package in disabled_packages[1:]:
                status_string += ',\n'
                status_string += ' ' * 20
                status_string += disabled_package
            status_string += ']\n'
        
        # Request processor status
        info = request_processor_services.get_info()
        status_string += 'Request Processor Parameters: {0}\n'.format(str(info))
        
        # Threads/Processes
        current_pid = os.getpid()
        current_process_thread_count = None
        # Reading current process' thread count.
        with open('/proc/{0}/status'.format(current_pid), 'r') as status_file:
            while True:
                file_line = status_file.readline()
                if not file_line:
                    break
                if file_line.startswith('Threads:'):
                    current_process_thread_count = int(file_line[8:].strip())
                    break
        
        status_string += 'Master Process Threads: {0}\n'.format(current_process_thread_count)
        
        # Finding all child processes.
        total_threads = 0
        total_children = 0
        for process_dir in os.listdir('/proc/'):
            if process_dir.isdigit() and os.path.isdir('/proc/{0}'.format(process_dir)):
                with open('/proc/{0}/status'.format(process_dir), 'r') as status_file:
                    while True:
                        file_line = status_file.readline()
                        if not file_line:
                            break
                        if file_line.startswith('PPid:'):
                            if int(file_line[5:].strip()) == current_pid:
                                # It's our child.
                                total_children += 1
                                # Continue to find threads.
                                while True:
                                    file_line = status_file.readline()
                                    if not file_line:
                                        break
                                    if file_line.startswith('Threads:'):
                                        total_threads += int(file_line[8:].strip())
                                        break
                            break
        
        status_string += 'Child Processes: {0}\n'.format(total_children)
        status_string += 'Child Threads: {0}\n'.format(total_threads)
        
        # TODO: Add database connections here.
        
        # Sessions
        status_string += 'Sessions: {0}'.format(session_services.get_sessions_count())

        return status_string
