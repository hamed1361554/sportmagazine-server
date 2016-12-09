"""
Created on Dec 1, 2016

@author: Hamed Zekri
"""

import decimal
import flask.json
from datetime import datetime


class CustomJsonEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.strftime("%Y-%M-%d %H:%M:%S")

        return super(CustomJsonEncoder, self).default(obj)