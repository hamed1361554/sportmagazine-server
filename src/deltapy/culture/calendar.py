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

import datetime

from deltapy.core import DeltaObject, DeltaException

class CalenderException(DeltaException):
    '''
    '''

class Calendar(DeltaObject):
    '''
    '''
    
    def __init__(self):
        self._holidays = {}
    
    def set_holidays(self, year, holidays):
        '''
        Sets the calneder holidays.
        
        @param year: year
        @param holidays: holdays
            [DynamicObject<month, day, [descriptions]> 
        '''
        
        for holiday in holidays:
            self._holidays[(year, holiday.month, holiday.day)] = holiday.descriptions
            
    def first_week_day(self):
        '''
        Returns first day of week
        
        @rtype: int
        '''
        
        return 0
        
    def to_local_date(self, dt):
        '''
        Returns date as local date. 
        
        @param dt: date
        
        @rtype: (year, month, day)
        '''
        
        return dt.year, dt.month, dt.day
    
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
        
        return datetime.datetime(year, month, day, hour, minute, second, microsecond)
    
    def add_days(self, dt, days):
        '''
        Adds specified days to given date.
        
        @param dt: date(or datetime)
        @param days: days
        
        @rtype: datetime
        '''
        
        return dt + datetime.timedelta(days = days)
    
    def add_weeks(self, dt, weeks):
        '''
        Adds specified weeks to given date.
        
        @param dt: date(or datetime)
        @param weeks: weeks
        
        @rtype: datetime
        '''
        
        return self.add_weeks(dt, weeks * 7)

    def add_months(self, dt, months):
        '''
        Adds specified months to given date.
        
        @param dt: date(or datetime)
        @param months: months
        
        @rtype: datetime
        '''
        
        local_year, local_month, local_day = self.to_local_date(dt)
        
        new_month = local_month + months
        new_year = local_year
        
        if new_month > 0:
            if new_month > 12:
                new_year += int(new_month / 12)
                new_month = new_month % 12
        else:
            new_year -= int(abs(new_month) / 12) + 1
            new_month = 12 - (abs(new_month) % 12)
            
                    
        local_year = new_year
        local_month = new_month
            
        max_days = self.days_of_month(local_year, local_month)
        if local_day > max_days:
            local_day = max_days
            
        return self.from_local_date(local_year, local_month, local_day, dt.hour, dt.minute, dt.second, dt.microsecond)

    def add_years(self, dt, years):
        '''
        Adds specified years to given date.
        
        @param dt: date(or datetime)
        @param years: years
        
        @rtype: datetime
        '''
        
        return self.add_months(dt, years * 12)
    
    def begin_of_day(self, dt):
        '''
        Adjusts date to begin of day.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        return self.trunc(dt)
    
    def end_of_day(self, dt):
        '''
        Adjust date to end of day.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        return self.trunc(self.add_days(dt, 1)) - datetime.timedelta(microseconds = 1)
    
    def begin_of_year(self, dt):
        '''
        Returns first day of year using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        year, month, day = self.to_local_date(dt)
        return self.from_local_date(year, 1, 1)
    
    def end_of_year(self, dt):
        '''
        Returns last day of year using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        year, month, day = self.to_local_date(dt)
        result = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(microseconds = -1) 
        return result

    def begin_of_month(self, dt):
        '''
        Returns first day of month using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
    
        year, month, day = self.to_local_date(dt)
        return self.from_local_date(year, month, 1)

    def end_of_month(self, dt):
        '''
        Returns last day of month using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        result = self.add_months(dt, 1)
        return datetime.datetime(result.year, result.month, 1) - datetime.timedelta(microseconds = -1)

    def begin_of_week(self, dt):
        '''
        Returns first day of week using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        week_day = dt.weekday()
        if week_day < self.first_week_day():
            days = 7 + week_day - self.first_week_day()
            result = self.add_days(dt, -days)
            return self.trunc(result)
        days = self.first_week_day() - week_day
        return self.trunc(self.add_days(dt, -days))
        
    def end_of_week(self, dt):
        '''
        Returns last day of week using given date.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        week_day = dt.weekday()
        if week_day > self.first_week_day():
            days = 6 - week_day + self.first_week_day()
            result = self.add_days(dt, days)
            return self.trunc(result)
        days = self.first_week_day() - week_day - 1
        return self.trunc(self.add_days(dt, days))

    def is_leap_year(self, year):
        '''
        Returns True if year of the given date is leap year.
        
        @param year: local year
        
        @rtype: bool
        '''
        
    def days_of_month(self, year, month):
        '''
        Returns number of days at given month.

        @param year: local year
        @param month: local month 
        
        @rtype: datetime
        '''
        
    def days_of_year(self, year):
        '''
        Returns number of days at given year.
        
        @param year: local year
        
        @rtype: datetime
        '''
        
    def trunc(self, dt):
        '''
        Removes hour, minute, second and microsecond form given date time value.
        
        @param dt: datetime
        
        @rtype: datetime
        '''
        
        return datetime.datetime(dt.year, dt.month, dt.day)
        
    def min(self):
        '''
        Returns available minimum datetime.
        
        @rtype: datetime
        '''
        
        return datetime.datetime(1972, 1, 1)
    
    def max(self):
        '''
        Returns available maximum datetime.

        @rtype: datetime
        '''

        return datetime.datetime(3000, 1, 1)
    
    def is_holiday(self, dt):
        '''
        Returns True if given day is holiday.
        
        @param dt: datetime
        
        @rtype: bool
        '''
        
        year, month, day = self.to_local_date(dt)
        return (year, month, day) in self._holidays

    def get_descriptions(self, dt):
        '''
        Returns descriptions of given date.
        
        @param dt: datetime
        
        @rtype: [str]
        '''
        
        return self._holidays.get(self.to_local_date(dt))
    
    def months_between(self, from_date, to_date):
        '''
        Returns months between given dates.
        
        @param from_date: from date
        @param to_date: to date
        
        @rtype: int
        '''
    
        a_dt = self.trunc(from_date)
        b_dt = self.trunc(to_date)
    
        if a_dt == b_dt:
            return 0
        
        if a_dt > b_dt:
            raise CalenderException('From date must be less than to date.')
            
        count = 0
        while True:
            a_dt = self.add_months(a_dt, 1)
            if a_dt >= b_dt:
                return count
            count = count + 1
    
    def days_between(self, from_date, to_date):
        '''
        Returns days between given dates.
        
        @param from_date: from date
        @param to_date: to date
        
        @rtype: int
        '''
    
        return (self.trunc(to_date) - self.trunc(to_date)).days
    
    # TODO: implement desire date in calendar
    def desire_date(self):
        pass
    
