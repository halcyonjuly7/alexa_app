import re
import math
import logging

class BaseFormatter:
    def __init__(self, source):
        self.source = source


class OmdbDataFormatter(BaseFormatter):

    def format_data(self, movie, data_source):
        formatted_target = data_source
        if re.match("[0-9]+\s\w+", data_source):
            formatted_target = self.minutes_to_hours(re.sub("\D+", "", data_source))
        logging.debug(formatted_target)
        adverb = "are" if "s" in self.source else "is"
        return "The {0} for {1}, {2} {3}".format(self.source, movie, adverb, formatted_target)

    def minutes_to_hours(self, min):
        raw_hours = int(min) / 60
        minutes, hour = math.modf(raw_hours)
        int_hour = int(hour)
        if not int_hour:
            return "{0} minutes".format(int(minutes * 60))
        hour_describer = "hours" if int_hour > 1 else "hour"
        return "{0} {1} and {2} minutes".format(int_hour, hour_describer, int(minutes * 60))

