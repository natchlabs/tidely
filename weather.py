import requests
import datetime

from dotenv import load_dotenv
load_dotenv()
import os

class WeatherResult():
    def __init__(self, expiryTime, data):
        self.expiryTime = expiryTime
        self.data = data
    
    def isExpired(self):
        return self.expiryTime <= datetime.datetime.now()

    def retrieveResult(self):
        return self.data        


class WeatherCache():
    def __init__(self):
        self.locations = {}

    def getWeather(self, locations):
        cachedLocationResults = []
        uncachedLocations = []
        for l in locations:
            if l['name'] in self.locations and not self.locations[l['name']].isExpired():
                cachedLocationResults.append(self.locations[l['name']].retrieveResult())
            else:
                uncachedLocations.append(l)
        
        if len(uncachedLocations) > 0:

            queryString = ';'.join(str(l['lat']) + ',' + str(l['lng']) for l in uncachedLocations)
            params = { 'q': queryString, 'format': 'json', 'key': os.environ.get('weather-key'), 'tide': 'yes', 'tp': '1' }

            result = requests.get(os.environ.get('weather-url'), params).json()
            retrievedLocationResults = [result['data']] if len(uncachedLocations) == 1 else result['data']['area']

            for index, r in enumerate(retrievedLocationResults):
                self.locations[locations[index]['name']] = WeatherResult(datetime.datetime.now() + datetime.timedelta(days=1), r)

            if len(uncachedLocations) == 1:
                cachedLocationResults.append(result['data'])
                return cachedLocationResults
            else:
                val = result['data']['area']
                val.extend(cachedLocationResults) 
                return val
        else:
            return cachedLocationResults

cache = WeatherCache()

def requestWeatherInformation(locations):
    return cache.getWeather(locations)
