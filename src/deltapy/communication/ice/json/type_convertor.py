'''
Created on Nov 15, 2009

@author: Abi.Mohammadi & Majid.Vesal
'''

from deltapy.core import DeltaObject, DynamicObject, DeltaException
from deltapy.communication.type_convertor import TypeConvertor

import deltapy.config.services as config_services

class InvalidCharacterForEncodingException(DeltaException):
    """

    """

class InvalidCharacterForDecodingException(DeltaException):
    """

    """

class StringConverter(DeltaObject):

    def __init__(self):
        DeltaObject.__init__(self)

        self._internal_encoding = config_services.get_app_config_store().get('global', 'encoding', 'utf-8')
        self._external_encoding = 'utf-8'

    def to_internal(self, text):
        try:
            if self._internal_encoding != self._external_encoding:
                if not isinstance(text, unicode):
                    text = text.decode(self._external_encoding)

                if self._internal_encoding == 'cp1256':
                    text = text.replace(u'\u06cc', u'\u064a')

                text = text.encode(self._internal_encoding)

            return text
        except UnicodeDecodeError as error:
            message = _('Error while decoding the given string from [{0}] format; '
                        'unsupported characters are observed.')
            exception = InvalidCharacterForDecodingException(message.format(self._external_encoding))
            exception.get_data()['faulty_string'] = text
            raise exception
        except UnicodeEncodeError as error:
            message = _('Error while encoding an string to [{0}] format; '
                        'unsupported characters are observed.')
            exception = InvalidCharacterForEncodingException(message.format(self._internal_encoding))
            exception.get_data()['faulty_string'] = text
            raise exception

    def to_external(self, text):
        try:
            if self._internal_encoding != self._external_encoding:
                if not isinstance(text, unicode):
                    text = text.decode(self._internal_encoding)
                text = text.encode(self._external_encoding)

            return text
        except UnicodeDecodeError as error:
            message = _('Error while decoding the given string from [{0}] format; '
                        'unsupported characters are observed.')
            exception = InvalidCharacterForDecodingException(message.format(self._internal_encoding))
            exception.get_data()['faulty_string'] = text
            raise exception
        except UnicodeEncodeError as error:
            message = _('Error while encoding an string to [{0}] format; '
                        'unsupported characters are observed.')
            exception = InvalidCharacterForEncodingException(message.format(self._external_encoding))
            exception.get_data()['faulty_string'] = text
            raise exception

class IceJsonTypeConvertor(TypeConvertor):
    '''
    Ice type convertor.
    '''
    
    def __init__(self):
        TypeConvertor.__init__(self)
        self._str_converter = StringConverter()

    def external_convert(self, obj):
        if isinstance(obj, DynamicObject):
            return dict(obj)
        return obj

    def internal_convert(self, obj):
        if isinstance(obj, str):
            return self._str_converter.to_internal(obj)
        elif isinstance(obj, dict):
            return DynamicObject(obj)
        return obj
