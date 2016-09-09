'''
Created on Nov, 2013

@author: Nastaran & Aidin
'''

from deltapy.event_system.decorators import before_handler
from deltapy.status_reporter.reporter import ServerStatusReporter

@before_handler('application.start', 'status reporter starter')
def start_reporter(*args):
    '''
    This will be called when application started.
    It starts the status reporter.
    '''
    ServerStatusReporter().run()
