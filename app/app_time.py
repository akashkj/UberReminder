"""
Wrapper time module to provide time fucntions for a particular timezone
"""
from datetime import datetime

import pytz


class Time(object):
    """
    Time module wrapper class to use in the application
    """

    ALL_TIMEZONES = pytz.all_timezones
    CURRENT_DATE_FORMAT = "%d-%m-%Y"
    CURRENT_DATETIME_FORMAT = "%d-%m-%Y %H:%M"

    def __init__(self, time_zone):
        self.time_zone = time_zone

    def now(self):
        """
        :return: datetime object for current time in given timezone
        """
        return datetime.now(tz=pytz.timezone(self.time_zone))

    def difference(self, datetime_one, datetime_two):
        """
        :param datetime_one: datetime object
        :param datetime_two: datetime onject
        :return: timedelta object difference of second and first argument
        """
        return (datetime_two - datetime_one).seconds / 60

    def string_to_time(self, time_string):
        """
        Converts string to time
        :param time_string: string
        :return: datetime object
        """
        hour, minute = map(int, time_string.split(":"))
        return self.now().replace(hour=hour, minute=minute)
