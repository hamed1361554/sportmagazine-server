# DeltaConsole, A console for DeltaPy applications.
# Copyright (C) 2009-2011  Aidin Gharibnavaz <aidin@aidinhut.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on Oct 5, 2009
@author: Abi.Mohammadi & Majid.Vesal

Modified by Aidin Gharibnavaz, March 11, 2010
  This module is borrowed from DeltaPy frame work,
  to handle the Type conversion between DObject and
  Python's objects.
'''

import Ice
import sys
import os
import datetime
import decimal
import traceback
from time import mktime, time

services_ice = os.path.join(os.path.abspath(os.path.dirname(sys.modules[__name__].__file__)), 'services.ice')
Ice.loadSlice(services_ice)
import DeltaIce
from DeltaIce import *

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
    
    if __internal_encoding__ != __external_encoding__:
        decoded = text.decode(__external_encoding__)
        if __internal_encoding__ == 'cp1256':
            decoded = decoded.replace(u'\u06cc', u'\u064a')
        return decoded.encode(__internal_encoding__)
    return text

def str_to_external(text):
    global __internal_encoding__
    global __external_encoding__

    if __internal_encoding__ != __external_encoding__:
        return text.decode(__internal_encoding__).encode(__external_encoding__)
    return text

__map_to_dtypes__ = None

def __make_dtype__(a):
    global __map_to_dtypes__
    if a is None:
        return None
    v_type, c_func = __map_to_dtypes__[a.__class__.__name__]
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
    dct = {}
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

def decimal_to_str(d):
    return str(d._round(30, 2))

def exception_to_errorobject(error, error_code = ''):
    '''
    Converts an exception to an ErrorObject.
    
    @param error: Should be of type Exception.
    @param error_code: A string that represents the code of the errror.
    '''
    result = DeltaIce.ErrorObject()
    
    result.message = str(error)
    result.traceback = traceback.format_exc()
    if __internal_encoding__ != __external_encoding__:
        result.message = result.message.decode(__internal_encoding__).encode(__external_encoding__)
        result.traceback = result.traceback.decode(__internal_encoding__).encode(__external_encoding__)
    result.code = error_code
    
    return result


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
                     'DynamicObject': (DictObject, dict_to_ddict)} 


