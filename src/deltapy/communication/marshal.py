'''
Created on Oct 15, 2014

@author: Abi.Mohammadi
'''

import json
import datetime
import array
import binascii

class JSONCustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            value = '{0:04d}{1:02d}{2:02d}{3:02d}{4:02d}{5:02d}{6:06d}'
            value = value.format(obj.year,
                                 obj.month,
                                 obj.day,
                                 obj.hour,
                                 obj.minute,
                                 obj.second,
                                 obj.microsecond) 
            return {'!JT' : 'dt',
                    '!V' : value}
        elif isinstance(obj, array.array):
            value = binascii.hexlify(obj)
            return {'!JT' : 'ar',
                    '!V' : value}
        elif isinstance(obj, Decimal):
            return {'!JT' : 'dc',
                    '!V' : str(obj)}
        else:
            return super(JSONCustomEncoder, self).default(obj)
        
class JSONCustomDecoder(json.JSONDecoder):
    def __init__(self, encoding=None):
        json.JSONDecoder.__init__(self, encoding=encoding,object_hook=self.dict_to_object)
    
    def dict_to_object(self, d): 
        if '!JT' not in d:
            return d

        json_type = d.pop('!JT')
        if json_type == 'dt':
            value = d['!V']
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
        
        if json_type == 'ar':
            data = d['!V']
            if data is None:
                return None
            result = array.array('B')
            unhex = binascii.unhexlify(data)
            result.fromstring(unhex)
            return result

        if json_type == 'dc':
            if d['!V'] is None:
                return None
            return Decimal(d['!V'])
        
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
