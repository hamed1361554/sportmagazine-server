'''
Created on Oct 5, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

import datetime
import decimal
import sys
import traceback
import array
import Ice
import os
import DeltaIce
from DeltaIce import *
from time import mktime, time

from deltapy.core import DynamicObject, DeltaException
from deltapy.utils import get_module_dir

class InvalidCharacterForEncodingException(DeltaException):
    """

    """

class InvalidCharacterForDecodingException(DeltaException):
    """

    """

Ice.loadSlice(os.path.join(get_module_dir('deltapy.communication.ice'), 'services.ice'))

__internal_encoding__ = 'utf-8'
__external_encoding__ = 'utf-8'

def set_encodings(internal, external):
    global __internal_encoding__
    global __external_encoding__

    __internal_encoding__ = internal
    __external_encoding__ = external

def str_to_internal(text):
    global __internal_encoding__
    global __external_encoding__
    try:

        if __internal_encoding__ != __external_encoding__:
            decoded = text.decode(__external_encoding__)
            if __internal_encoding__ == 'cp1256':
                decoded = decoded.replace(u'\u06cc', u'\u064a')
            return decoded.encode(__internal_encoding__)

        return text
    except UnicodeDecodeError as error:
        message = _('Error while decoding the given string from [{0}] format; '
                    'unsupported characters are observed.')
        exception = InvalidCharacterForDecodingException(message.format(__external_encoding__))
        exception.get_data()['faulty_string'] = text
        raise exception
    except UnicodeEncodeError as error:
        message = _('Error while encoding an string to [{0}] format; '
                    'unsupported characters are observed.')
        exception = InvalidCharacterForEncodingException(message.format(__internal_encoding__))
        exception.get_data()['faulty_string'] = text
        raise exception

def str_to_external(text):
    global __internal_encoding__
    global __external_encoding__

    try:
        if __internal_encoding__ != __external_encoding__:
            return text.decode(__internal_encoding__).encode(__external_encoding__)
        return text
    except UnicodeDecodeError as error:
        message = _('Error while decoding the given string from [{0}] format; '
                    'unsupported characters are observed.')
        exception = InvalidCharacterForDecodingException(message.format(__internal_encoding__))
        exception.get_data()['faulty_string'] = text
        raise exception
    except UnicodeEncodeError as error:
        message = _('Error while encoding an string to [{0}] format; '
                    'unsupported characters are observed.')
        exception = InvalidCharacterForEncodingException(message.format(__external_encoding__))
        exception.get_data()['faulty_string'] = text
        raise exception

__map_to_dtypes__ = None

def __make_dtype__(a):
    global __map_to_dtypes__

    if a is None:
        return None

    class_name = a.__class__.__name__

    # To avoid problems on 64bit systems which oracle client returns int object for large
    # numbers. (The number that checked is the maximum log value in C++)
    if class_name == 'int' and (abs(a) > 2147483647):
        class_name = 'float'
        a = float(a)

    if isinstance(a, DynamicObject):
        class_name = 'DynamicObject'
    v_type, c_func = __map_to_dtypes__[class_name]
    v = v_type()
    if c_func:
        v.value = c_func(a)
    else:
        v.value = a
    return v 

def list_to_dlist(lst):
    if lst is None:
        return None
    dlst = []
    for a in lst:
        dlst.append(__make_dtype__(a))
    return dlst

def dict_to_ddict(dct):
    if dct is None:
        return None
    ddct = {}
    for k in dct:
        v = dct[k]
        ddct[k] = __make_dtype__(v)
    return ddct

def object_to_dobject(obj):
    if obj is None:
        return None
    return __make_dtype__(obj)

def dbuffer_to_buffer(dbuf):
    return str(buffer(array.array('B', dbuf.value)))

def dobject_to_object(dobj):
    if dobj is None:
        return None
    if dobj.__class__ is list:
        return dlist_to_list(dobj)
    elif dobj.__class__ is tuple:
        return dlist_to_list(dobj)
    elif dobj.__class__ is dict:
        return ddict_to_dict(dobj)
    elif dobj.__class__ is ListObject:
        return dlist_to_list(dobj.value)
    elif dobj.__class__ is DictObject:
        return ddict_to_dict(dobj.value)
    elif dobj.__class__ is DateTimeObject:
        return datetime.datetime(dobj.value.year, 
                                 dobj.value.month, 
                                 dobj.value.day, 
                                 dobj.value.hour, 
                                 dobj.value.minute, 
                                 dobj.value.second, 
                                 dobj.value.microsecond)
    elif dobj.__class__ is BufferObject:
        return dbuffer_to_buffer(dobj)
    elif dobj.__class__ is StringObject:
        return str_to_internal(dobj.value)
    elif dobj.__class__ is DecimalObject:
        return decimal.Decimal(dobj.value)
    else:
        return dobj.value

def dlist_to_list(dlst):
    '''
    Converts a DList object to Python list.
    
    @param dlst: DList
    '''
    
    if dlst is None:
        return None
    lst = []
    for a in dlst:
        lst.append(dobject_to_object(a))
    return lst

def ddict_to_dict(ddct):
    '''
    Converts a DDictionary object to Python dictionary.
    
    @param ddct: DDictionary
    '''
    if ddct is None:
        return None
    dct = DynamicObject()
    for k in ddct:
        v = ddct[k]
        dct[k] = dobject_to_object(v)
    return dct

   
def datetime_to_float(dt):
    try:
        return mktime(dt.timetuple())+1e-6*dt.microsecond
    except:
        return time()

def datetime_to_ddatetime(dt):
    value = DateTimePure()
    value.year = dt.year
    value.month = dt.month
    value.day = dt.day
    value.hour = dt.hour
    value.minute = dt.minute
    value.second = dt.second
    value.microsecond = dt.microsecond
    return value

def buffer_to_dbuffer(buf):
    return str(buf)

TEN_IN_DECIMAL = decimal.Decimal(10)

def decimal_to_str(d):
    return str(d.quantize(TEN_IN_DECIMAL ** (-2)))

def array_to_darray(arr):
    return arr

__map_to_dtypes__ = {'int': (IntObject, None),
                     'str': (StringObject, str_to_external),
                     'double': (DoubleObject, None),
                     'long': (LongObject, None),
                     'bool': (BoolObject, None),
                     'float': (DoubleObject, None),
                     'datetime': (DateTimeObject, datetime_to_ddatetime),
                     'Decimal': (DecimalObject, decimal_to_str),
                     'dict': (DictObject, dict_to_ddict),
                     'list': (ListObject, list_to_dlist),
                     'tuple': (ListObject, list_to_dlist),
                     'buffer': (BufferObject, buffer_to_dbuffer),
                     'array' : (BufferObject, array_to_darray),
                     'DynamicObject': (DictObject, dict_to_ddict)} 

