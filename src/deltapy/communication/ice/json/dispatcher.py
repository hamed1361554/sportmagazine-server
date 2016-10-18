'''
Created on Dec 24, 2012

@author: Abi.Mohammadi & Majid.Vesal
'''

import json
import datetime
import traceback
import array
from decimal import Decimal

import DeltaIce

from deltapy.core import DeltaException
from deltapy.communication.listener import Dispatcher
from deltapy.communication.ice import utils


class JSONCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            value = '{0:04d}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}{6:06d}'#obj.strftime("%b %d, %Y %H:%M:%S %p")
            value = value.format(obj.year,
                                 obj.month,
                                 obj.day,
                                 obj.hour,
                                 obj.minute,
                                 obj.second,
                                 obj.microsecond) 
            return {'__JSON_TYPE__' : 'datetime',
                    'value' : value}
        elif isinstance(obj, array.array):
            return {'__JSON_TYPE__' : 'byte_array',
                    'value' : obj.tolist()}
        elif isinstance(obj, Decimal):
            return {'__JSON_TYPE__' : 'decimal',
                    'value' : str(obj)}
        else:
            return super(JSONCustomEncoder, self).default(obj)
        
class JSONCustomDecoder(json.JSONDecoder):
    def __init__(self, encoding=None):
        json.JSONDecoder.__init__(self, encoding=encoding,object_hook=self.dict_to_object)
    
    def dict_to_object(self, d): 
        if '__JSON_TYPE__' not in d:
            return d

        json_type = d.pop('__JSON_TYPE__')
        if json_type == 'datetime':
            value = d['value']
            if value is None:
                return None
            dt = datetime.datetime.strptime(value[0:-6], '%Y%m%d%H%M%S')
            microsecond = int(value[-6:])
            return datetime.datetime(dt.year, 
                                     dt.month, 
                                     dt.day, 
                                     dt.hour, 
                                     dt.minute, 
                                     dt.second, 
                                     microsecond)
        
        if json_type == 'byte_array':
            if d['value'] is None:
                return None
            return array.array.fromlist(d['value'])

        if json_type == 'decimal':
            if d['value'] is None:
                return None
            return Decimal(d['value'])
        
        raise DeltaException('Unknown json type [{0}]'.format(json_type))
    
def convert(input, encoding = 'utf-8'):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode(encoding)
    else:
        return input

class IceJsonDispatcher(DeltaIce.IIceJsonDispatcher, Dispatcher):
    
    def __init__(self, listener):
        Dispatcher.__init__(self, listener)

    def _get_client_ip_(self, **options):
        current = options.get('current')
        if current is not None:
            ip_port = current.con.toString().split('remote address = ')[1]
            ip_address = ip_port.split(':')[0]
            return ip_address
    
    def login(self, userName, password, options, current = None):
        try:
            t_options = \
                convert(json.loads(options, cls=JSONCustomDecoder))
            result = \
                self._listener.login(self._get_client_ip_(current = current), 
                                     userName, 
                                     password,
                                     **t_options)
            return json.dumps(result, cls=JSONCustomEncoder)
        except DeltaException, error:
            exception = DeltaIce.JsonAuthenticationException()
            exception.code = error.get_code()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception, error:
            exception = DeltaIce.JsonGenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        
    def loginEx(self, userName, password, options, current = None):
        try:
            t_options = \
                convert(json.loads(options, cls=JSONCustomDecoder))
            result = \
                self._listener.login_ex(self._get_client_ip_(current = current), 
                                        userName, 
                                        password,
                                        **t_options)
            return json.dumps(result, cls=JSONCustomEncoder)
        except DeltaException, error:
            exception = DeltaIce.JsonAuthenticationException()
            exception.code = error.get_code()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception, error:
            exception = DeltaIce.JsonGenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        
    def logout(self, ticket, userName, current = None):
        try:
            return self._listener.logout(self._get_client_ip_(current = current), 
                                         ticket, 
                                         userName)
        except Exception, error:
            exception = DeltaIce.JsonGenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
    
    def execute(self, ticket, userName, commandKey, args, kwargs, current = None):
        try:
            t_args = \
                convert(json.loads(args, cls=JSONCustomDecoder))
            t_kwargs = \
                convert(json.loads(kwargs, cls=JSONCustomDecoder))
            result = \
                 self._listener.execute(self._get_client_ip_(current = current),
                                        ticket, 
                                        userName, 
                                        commandKey,
                                        *t_args,
                                        **t_kwargs)
            return json.dumps(result, cls=JSONCustomEncoder, encoding='cp1256')
        except DeltaException, error:
            exception = DeltaIce.JsonGenericException()
            exception.code = error.get_code()
            exception.data = json.dumps(error.get_data(), cls=JSONCustomEncoder, encoding='cp1256')
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception, error:
            exception = DeltaIce.JsonGenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
    
    def executeEx(self, request, current = None):
        try:
            t_request = \
                convert(json.loads(request, cls=JSONCustomDecoder))
            t_request['ip'] = self._get_client_ip_(current = current)
            result = \
                self._listener.execute_ex(t_request)
            return json.dumps(result, cls=JSONCustomEncoder, encoding='cp1256')
        except DeltaException, error:
            exception = DeltaIce.JsonGenericException()
            exception.code = error.get_code()
            exception.data = json.dumps(error.get_data(), cls=JSONCustomEncoder, encoding='cp1256')
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
        except Exception, error:
            exception = DeltaIce.JsonGenericException()
            exception.message = utils.str_to_external(str(error))
            exception.traceback = utils.str_to_external(traceback.format_exc())
            raise exception
    
