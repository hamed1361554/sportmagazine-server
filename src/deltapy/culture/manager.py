# Copyright (c) 2000 - 2010 Majid Vesal <mva_vesal@yahoo.com> and
# Abi M.Sangarab <abisxir@gmail.com>
#
# This file is part of Deltapy.

# Deltapy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# Deltapy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Deltapy. If not, see <http://www.gnu.org/licenses/>.
'''
Created on Nov 16, 2010

@author: abi
'''

import gettext
import os

from deltapy.core import DeltaObject, DeltaException
from deltapy.application.services import get_application_dir
from deltapy.culture.deltapy_gettext import DeltaPyTranslation

class CultureManagerException(DeltaException):
    '''
    '''
    
class CultureManager(DeltaObject):
    '''
    '''
    
    def __init__(self):
        self._calendars = {}
        self._locale = None
        
    def set_locale(self, locale, **options):
        '''
        Sets the application locale.
        
        @param locale: locale
        '''
        
        locale_dir = os.path.join(get_application_dir(), 'locale')
        language = gettext.translation("messages",
                                       locale_dir,
                                       languages=[locale],
                                       codeset=options.get('encoding'),
                                       class_=DeltaPyTranslation)
        language.setup(options.get('encoding'), locale_dir, locale)
        language.install()
        self._locale = locale
        
    def get_locale(self):
        '''
        Returns the application default locale.
        
        @rtype: str
        '''
        
        return self._locale
    
    def register_calendar(self, locale, calendar):
        '''
        Registers the given calendar.
        
        @param calendar: calendar instance
        '''
        
        self._calendars[locale] = calendar
        
    def get_calendars(self):
        '''
        Returns available calendars.
        
        @rtype: [Calendar] 
        '''
        
        return self._calendars.values()
    
    def get_calendar(self, locale = None, **options):
        '''
        Returns the specified locale calendar.
        If locale is None it returns default calendar.
        
        @rtype: Calendar
        '''
        
        if locale is None:
            locale = self.get_locale()

        calendar = self._calendars.get(locale)
        if calendar is None:
            message = _('Could not find any calendar for locale [{locale}].')
            raise CultureManagerException(message.format(locale = locale))
        
        return calendar
