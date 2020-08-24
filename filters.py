import functools
import itertools as it
import datetime
class WeatherMatcher:
    """WeatherMatchers filter through weather result based on a specific attribute

    Weather results are returned from the worldweatheronline API as hourly chunks. A WeatherMatcher
    can be used as a predicate to test whether a given chunk passes the user's requirements based on
    one attribute of the weather (e.g. temperature). WeatherMatchers can be used in combination in a
    WeatherConfiguration to test chunks based on multiple attributes.
    """

    def __init__(self, prop, lower, upper):
        self.prop = prop
        self.lower = lower
        self.upper = upper

    def testChunk(self, weatherChunk):
        return self.lower <= float(weatherChunk[self.prop]) <= self.upper

    def changeBounds(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __call__(self, weatherChunk):
        return self.testChunk(weatherChunk)
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

    def testChunk(self, weatherChunk):
        return functools.reduce(lambda acc,cur: cur(weatherChunk) and acc, self.matchers, True)
    
    def mergeChunks(self, chunks):
        startTime = chunks[0]['time']
        endTime = startTime + datetime.timedelta(hours=len(chunks))
        return {
            'startTime': str(startTime),
            'endTime': str(endTime),
            'activity': self.activity,
            'location': chunks[0]['location'],
            'weather': {
                'desc': chunks[0]['weatherDesc'],
                'icon': chunks[0]['weatherIconUrl']
            }
        }

    def __call__(self, weatherChunks):
        validSections = [list(groups) for key, groups in it.groupby(weatherChunks, self.testChunk) if key]
        elements = [self.mergeChunks(x) for x in validSections]
        return elements
    
    def updateMatchers(self, matchers):
        self.matchers = matchers