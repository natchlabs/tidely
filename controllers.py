import pycurl
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()
import os
import json

import parse
from filters import WeatherMatcher, WeatherConfiguration
from locations import geocode

def getWeatherForUnknownLocations(locationNames, configurations):
    """Given a list of location names and a list of WeatherConfigurations, return activity recommendations

    This function represents the culmination of the application. It geocodes each of the names in the list
    of location names, uses the results to make a call to the worldweatheronline bulk API, and finally applies
    the WeatherConfiguration objects to the results from this API call. This returns a list of activity
    recommendations in a format suitable for the end-user.
    """

    locationCoords = geocode(locationNames)
    return getWeatherForKnownLocations(locationNames, locationCoords, configurations)

def getWeatherForKnownLocations(locations, configurations):
    """ Given a list of location names and their coordinates, return activity recommendations"""

    queryString = ';'.join(str(l['lat']) + ',' + str(l['lng']) for l in locations)
    params = f"?q={queryString}&format=json&key={os.environ.get('weather-key')}&tide=yes"

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://api.worldweatheronline.com/premium/v1/marine.ashx' + params)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    r = json.loads(body)
    
    return parse.handleAPICallBulk(r['data'], [l['name'] for l in locations], configurations)