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

from deltapy.application.services import get_component
from deltapy.culture import CULTURE_MANAGER

def register_calendar(locale, calendar):
    '''
    Registers the given calendar.
    
    @param calendar: calendar instance
    '''
    
    return get_component(CULTURE_MANAGER).register_calendar(locale, calendar)
    
def get_calendars():
    '''
    Returns available calendars.
    
    @rtype: [Calendar] 
    '''

    return get_component(CULTURE_MANAGER).get_calendars()

def get_calendar(locale = None, **options):
    '''
    Returns the specified locale calendar.
    If locale is None it returns default calendar.
    
    @rtype: Calendar
    '''

    return get_component(CULTURE_MANAGER).get_calendar(locale = None, **options)

def set_locale(locale):
    '''
    Sets the application locale.
    
    @param locale: locale
    '''
    
    return get_component(CULTURE_MANAGER).set_locale(locale)
    
def get_locale():
    '''
    Returns the application default locale.
    
    @rtype: str
    '''
    
    return get_component(CULTURE_MANAGER).get_locale()
