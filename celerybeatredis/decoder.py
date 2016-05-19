#! /usr/bin/env python
# coding: utf-8
# Date: 14/8/31
# Author: konglx
# File:
# Description:
from datetime import datetime

try:
    import simplejson as json
except ImportError:
    import json

from .globals import PY3


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                                  *args, **kargs)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            if type == 'datetime':
                dateobj = datetime(**d)
                return dateobj
            elif type == 'set':
                return set(d['objects'])
            else:
                d['__type__'] = type
                return d
        except:
            d['__type__'] = type
            return d


class DateTimeEncoder(json.JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder.
        Also handle when running Python 3 which isn't able to serialize
        sets in json by default
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            if PY3:
                if isinstance(obj, set):
                    return {
                        '__type__': 'set',
                        'objects': list(obj)
                    }
                else:
                    return json.JSONEncoder.default(self, obj)
            else:
                return json.JSONEncoder.default(self, obj)
