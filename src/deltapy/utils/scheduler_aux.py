'''
Created on Aug 19, 2009

@author: mohammadi, vesal
'''

import datetime

def every_x_secs(x):
    """
    Returns a function that will generate a datetime object that is x seconds
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(seconds=x)
    
def every_x_mins(x):
    """
    Returns a function that will generate a datetime object that is x minutes
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(minutes=x)    

def every_x_hours(x):
    """
    Returns a function that will generate a datetime object that is x hours
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(hours=x)

def every_x_weeks(x):
    """
    Returns a function that will generate a datetime object that is x weeks
    in the future from a given argument.
    """
    return lambda last: last + datetime.timedelta(weeks=x)

def daily_at(time):
    """
    Returns a function that will generate a datetime object that is one day
    in the future from a datetime argument combined with 'time'.
    """
    return lambda last: datetime.datetime.combine(last + datetime.timedelta(days=1), time)
    