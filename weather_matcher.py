import functools
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
