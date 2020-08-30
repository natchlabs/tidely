import requests

from dotenv import load_dotenv
load_dotenv()
import os

import parse
from filters import WeatherMatcher, WeatherConfiguration
from locations import geocode

def getWeather(locationNames, configurations):
    """Given a list of locations and a list of WeatherConfigurations, return activity recommendations

    This function represents the culmination of the application. It geocodes each of the names in the list
    of location names, uses the results to make a call to the worldweatheronline bulk API, and finally applies
    the WeatherConfiguration objects to the results from this API call. This returns a list of activity
    recommendations in a format suitable for the end-user.
    """

    queryString = ';'.join(geocode(locationNames)) # querystring for the worldweatheronline api
    params = { 'q': queryString, 'format': 'json', 'key': os.environ.get('weather-key'), 'tide': 'yes' }
    
    r = requests.get(os.environ.get('weather-url'), params).json()
    # as the format for the worldweatheronline api is different if there is one location, the response handling method is chosen
    # note: this should be refactored so that the response handlers can make this decision themselves
    return parse.handleAPICallBulk(r['data'], [l['name'] for l in locations], configurations)