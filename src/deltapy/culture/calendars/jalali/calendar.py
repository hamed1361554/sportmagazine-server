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
from deltapy.commander.decorators import command

import datetime

from deltapy.culture.calendar import Calendar
import deltapy.culture.calendars.util as calendar_util

class JalaliCalendar(Calendar):
    '''
    '''
    
    def first_week_day(self):
        '''
        Returns first day of week
        
        @rtype: int
        '''
        
        return 5

    def to_local_date(self, dt):
        '''
        Returns date as local date. 
        
        @param dt: date
        
        @rtype: (year, month, day)
        '''

        jdt = calendar_util.gregorian_to_jd(dt.year, dt.month, dt.day)

        return calendar_util.jd_to_persian(jdt)
    
    def from_local_date(self, year, month, day, hour = 0, minute = 0, second = 0, microsecond = 0):
        '''
        Returns system date by given local date values.
        
        @param year: year
        @param month: month
        @param day: day
        @param hour: hour
        @param minute: minute
        @param second: second
        @param microsecond: micorsecond
        
        @rtype: datetime
        '''
        
        jdt = calendar_util.persian_to_jd(year, month, day)
        g_year, g_month, g_day = calendar_util.jd_to_gregorian(jdt)
        return datetime.datetime(g_year, g_month, g_day, hour, minute, second, microsecond)
    
    def is_leap_year(self, year):
        '''
        Returns True if year of the given date is leap year.
        
        @param year: local year
        
        @rtype: bool
        '''
        
        return calendar_util.leap_persian(year)
        
    def days_of_month(self, year, month):
        '''
        Returns number of days at given month.

        @param year: local year
        @param month: local month 
        
        @rtype: datetime
        '''
        
        if month < 7:
            return 31
        elif month < 12 or self.is_leap_year(year):
            return 30
        return 29        
        
    def days_of_year(self, year):
        '''
        Returns number of days at given year.
        
        @param year: local year
        
        @rtype: datetime
        '''
        