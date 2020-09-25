import functools
import itertools as it
import datetime
import parse
from abc import ABC
from dateutil import parser

from dotenv import load_dotenv
load_dotenv()
import os

class WeatherMatcher(ABC):
    """WeatherMatchers filter through weather result based on a specific attribute

    Weather results are returned from the worldweatheronline API as hourly chunks. A WeatherMatcher
    can be used as a predicate to test whether a given chunk passes the user's requirements based on
    one attribute of the weather (e.g. temperature). WeatherMatchers can be used in combination in a
    WeatherConfiguration to test chunks based on multiple attributes.
    """

    def testChunk(self, weatherChunk):
        """Takes a single weather chunk and determines whether it passes the filter or not"""

    def __call__(self, weatherChunk):
        return self.testChunk(weatherChunk)

class BoundMatcher(WeatherMatcher):
    def __init__(self, prop, lower, upper):
        self.prop = prop
        self.lower = lower
        self.upper = upper

    def testChunk(self, weatherChunk):
        return self.lower <= float(weatherChunk[self.prop]) <= self.upper

class TideMatcher(WeatherMatcher):
    def __init__(self, aroundLow, berth):
        self.aroundLow = aroundLow
        self.berth = berth

    def testChunk(self, weatherChunk):
        tides = weatherChunk['dayWeather']['tides'][0]['tide_data']
        for tide in tides:
            if self.tideSuitable(weatherChunk['time'], tide):
                return True
        return False
    
    def tideSuitable(self, chunkTime, tide):
        rightType = (tide['tide_type'] == 'LOW' and self.aroundLow) or (tide['tide_type'] == 'HIGH' and not self.aroundLow)
        difference = chunkTime - parser.parse(tide['tideTime'])
        return rightType and abs(difference.total_seconds()) % (24 * 3600) < self.berth * 60

class WeatherCodeMatcher(WeatherMatcher):
    def __init__(self, codes):
        self.codes = codes
    
    def testChunk(self, weatherChunk):
        return int(weatherChunk['weatherCode']) in self.codes

class TimeMatcher(WeatherMatcher):
    def __init__(self, earliest, latest):
        self.earliest = earliest
        self.latest = latest
    
    def testChunk(self, weatherChunk):
        return self.earliest <= weatherChunk['time'].hour < self.latest

class WeatherConfiguration:
    """WeatherConfigurations represent a collection of WeatherMatchers for multi-attribute filtering

    One WeatherConfiguration object represents the set of WeatherMatchers for a given activity for a given
    user.

    WeatherConfigurations can take a given weather chunk and test it with multiple WeatherMatchers.
    Additionally, WeatherConfigurations can act as callables which can take a list of weather chunks.
    In this case, the weather chunks will be transformed into a formatted list which filters for only chunks
    which pass the WeatherMatchers, merges adjacent (in terms of time) chunks together after the filter, and
    formats the chunks to be nicely presentable to the user.
    """

    def __init__(self, activity, matchers):
        self.matchers = matchers
        self.activity = activity
        self.currentlyBuilding = {}

    def testChunk(self, weatherChunk):
        if weatherChunk['time'] < datetime.datetime.now() - datetime.timedelta(hours=1):
            return (False, None)
        matched = all(m(weatherChunk) for m in self.matchers)
        if matched:
            return (True, weatherChunk['time'].day)
        return (False, None)
    
    def mergeChunks(self, chunks):
        today = datetime.datetime.now().date()
        startTime = chunks[0]['time']
        endTime = startTime + datetime.timedelta(hours=len(chunks))
        date = self.getDay(startTime)

        # generate the various pieces of data, nicely formatted, as needed by the user
        astronomy = chunks[0]['dayWeather']['astronomy']
        day = parser.parse(astronomy[0]['sunrise']).hour <= chunks[0]['time'].hour < parser.parse(astronomy[0]['sunset']).hour
        timePeriod = 'day' if day else 'night'
        icon = os.environ.get('firebase-url') + timePeriod + '%2F' + chunks[0]['weatherCode'] + '.png' + os.environ.get('firebase-params')

        return {
            'isoStart': startTime,
            'startTime12h': startTime.strftime('%I:%M%p'),
            'startTime24h': startTime.strftime('%H:%M'),
            'endTime12h': endTime.strftime('%I:%M%p'),
            'endTime24h': endTime.strftime('%H:%M'),
            'startTimeInt': startTime.hour,
            'endTimeInt': endTime.hour,
            'date': date,
            'dateFromTodayInt': (startTime.date() - today).days,
            'activity': self.activity,
            'locations': [chunks[0]['location']],
            'weather': {
                'desc': chunks[0]['weatherDesc'][0]['value'],
                'icon': icon
            }
        }

    def getDay(self, day):
        return ('Today' if day.date() == datetime.date.today() else
            'Tomorrow' if day.date() == datetime.date.today() + datetime.timedelta(days=1) else day.date().strftime('%A'))

    def __call__(self, weatherChunks):
        # group the weather chunks based on whether the passed the tests and whether they are on the same day
        validSections = [list(groups) for key, groups in it.groupby(weatherChunks, self.testChunk) if key[0]]

        output = []
        for section in validSections:
            timeframe = (section[0]['time'], len(section))
            if timeframe in self.currentlyBuilding:
                self.currentlyBuilding[timeframe]['locations'].append(section[0]['location'])
                continue
            result = self.mergeChunks(section)
            output.append(result)
            self.currentlyBuilding[timeframe] = result

        return output
    
    def reset(self):
        self.currentlyBuilding = {}
    
    def updateMatchers(self, matchers):
        self.matchers = matchers

def getBounds(configurations):
    bounds = {}

    for configuration in configurations:
        for matcher in configuration.matchers:
            if isinstance(matcher, TimeMatcher):
                bounds[configuration.activity] = matcher.earliest, matcher.latest
                break
    return bounds