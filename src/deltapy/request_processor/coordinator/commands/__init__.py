'''
Created on Mar 3, 2013

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.commander.decorators import command
import deltapy.request_processor.coordinator.services as coordinator_services

#@command('request_processor.coordinator.transaction.state')
def get_transaction_state(transaction_id):
    '''
    Returns transaction state.
    
    @param str transaction_id: transaction ID
    
    @rtype: int
    @note: 
        0: Completed
        1: Failed
        2: Reversed
        3: Reverse Failed
    @return: transaction state
    '''
    
    return coordinator_services.get_transaction_state(transaction_id)
    
@command('request_processor.coordinator.request.state')
def get_request_state(request_id):
    '''
    Returns state of specified request.
    
    @param str request_id: request ID
    
    @rtype: int
    @note: 
        0: Received
        1: Completed
        2: Failed
    @return: request state
    '''
    
    return coordinator_services.get_request_state(request_id)    
    
#@command('request_processor.coordinator.transaction.detail')
def get_transaction_detail(transaction_id):
    '''
    Returns detail information of the specified transaction.
    
    @param str transaction_id: transaction ID
    
    @rtype: dict(str transaction_id: transaction ID
                 int state: transaction state,
                 datetime start_date: start date of transaction,
                 str user_id: user ID,
                 list requests: requests regarding to the transaction)
    @type requests: dict(str request_id: request ID,
                         int state: request state,
                         object input: request input,
                         object result: request result)
                         
    @return: transaction detail
    '''
    
    return coordinator_services.get_transaction_detail(transaction_id)    
    
#@command('request_processor.coordinator.activate_channel')
def activate_channel(channel_id):
    '''
    Activates transaction coordination on the given channel. 
    
    @param str channel_id: channel ID
    '''
    
    return coordinator_services.activate_channel(channel_id)
    
#@command('request_processor.coordinator.activate_service')
def activate_service(service_id):
    '''
    Activates transaction coordination on the given service.
    
    @param str service_id: service ID
    '''
           
    return coordinator_services.activate_service(service_id)

#@command('request_processor.coordinator.deactivate_channel')
def deactivate_channel(channel_id):
    '''
    Deativates transaction coordination on the given channel. 
    
    @param str channel_id: channel ID
    '''
    
    return coordinator_services.deactivate_channel(channel_id)

#@command('request_processor.coordinator.deactivate_service')
def deactivate_service(service_id):
    '''
    Dectivates transaction coordination on the given service.
    
    @param str service_id: service ID
    '''
    
    return coordinator_services.deactivate_service(service_id)

