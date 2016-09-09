'''
Created on Feb 2, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''
from deltapy.commander.decorators import command
import deltapy.request_processor.services as request_processor

@command('request_processor.resize')
def resize(size):
    '''
    Resizes current process pool.
    @param size: size of parallel requests.
    '''
    return request_processor.resize(size)

@command('request_processor.info')
def get_info():
    '''
    Returns information about active request processor.
    
    @return: DynamicObject
    '''
    
    return request_processor.get_info()

@command('request_processor.timeout.set')
def set_timeout(timeout):
    '''
    Sets global timeout of request processor.
    
    @param timeout: timeout
    '''
    
    return request_processor.set_timeout(timeout)
    
@command('request_processor.timeout.get')
def get_timeout():
    '''
    Returns get global timeout value.
    
    @rtype: int
    @return: timeout value
    '''

    return request_processor.get_timeout()
