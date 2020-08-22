import functools
import itertools as it
import datetime
def parseResponse(response):
    return [combine(hourly, 'time', toDatetime(day['date'], hourly['time'])) for day in response['data']['weather'] for hourly in day['hourly']]

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

def toDatetime(date, time):
    d = [int(a) for a in date.split('-')]
    return datetime.datetime(*d, int(int(time) / 100), tzinfo=LOCAL_TIMEZONE)

def combine(thing, key, value):
    thing[key] = value
    return thing
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
    
    def mergeChunks(self, chunks, location):
        startTime = chunks[0]['time']
        endTime = startTime + datetime.timedelta(hours=len(chunks))
        return {
            'startTime': str(startTime),
            'endTime': str(endTime),
            'activity': self.activity,
            'location': location,
            'weather': {
                'desc': chunks[0]['weatherDesc'],
                'icon': chunks[0]['weatherIconUrl']
            }
        }

    def __call__(self, weatherChunks, location):
        validSections = [list(groups) for key, groups in it.groupby(weatherChunks, self.testChunk) if key]
        elements = [self.mergeChunks(x, location) for x in validSections]
        return elements
    
    def updateMatchers(self, matchers):
        self.matchers = matchers
