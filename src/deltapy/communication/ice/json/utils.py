__author__ = 'ehsan'

import array
import datetime
import decimal

from DeltaIce import *

from deltapy.communication.ice.utils import dlist_to_list, ddict_to_dict, str_to_internal


def dbuffer_to_buffer(dbuf):
    return array.array('B', dbuf.value)

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