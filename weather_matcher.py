import functools
import itertools as it
import datetime

import tidely_parse as p


class WeatherMatcher:
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
