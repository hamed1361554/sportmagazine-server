'''
Created on Feb, 2015

@author: Aidin
'''

import sys
import signal
from threading import Event

from deltapy.application.services import get_app
import deltapy.request_processor.services as request_processor_services
import deltapy.config.services as config_services


def terminate():
    sys.exit(0)

def worker_process_main_func(child_number, max_threads):
    '''
    @param child_number: Number of this process in the sequence
        of processes.
    '''
    
    # Step one, starting a multithread request processor.
    request_processor_services.start(processor_name='multithread',
                                     max_threads=max_threads)

    # Step two, starting the communicator.
    config_name = "{0}.communication".format(get_app().get_name()) 
    config_store = config_services.get_config_store(config_name)

    for section in config_store.get_sections():
        if section == 'global':
            continue
        
        original_port = int(config_store.get(section, 'port'))
        config_store.set(section, 'port', str(original_port + child_number))

    # Imported here to prevent circular dependency.
    import deltapy.communication.services as communication_services
    
    communication_services.start(config_store)

    # Handling term signal
    signal.signal(signal.SIGTERM, terminate)

    # Wait forever...
    Event().wait()
