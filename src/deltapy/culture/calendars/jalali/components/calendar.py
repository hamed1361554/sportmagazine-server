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

from deltapy.culture.calendars.jalali.calendar import JalaliCalendar
from deltapy.application.decorators import register
from deltapy.culture.calendars.jalali import JALALI_CALENDAR
from deltapy.culture.services import register_calendar

@register(JALALI_CALENDAR)
class JalaliCalendarComponent(JalaliCalendar):
    '''
    '''
    
    def __init__(self):
        '''
        '''
        
        register_calendar("fa_IR", self)
    
