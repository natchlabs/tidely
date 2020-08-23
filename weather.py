import requests

from dotenv import load_dotenv
load_dotenv()
import os

import tidely_parse as parse
from weather_matcher import WeatherMatcher, WeatherConfiguration
import locations

def getWeather(locationNames, configurations):
    queryString = ';'.join(locations.geocode(locationNames))
    params = { 'q': queryString, 'format': 'json', 'key': os.environ.get('weather-key'), 'tide': 'yes' }
    
    r = requests.get(os.environ.get('weather-url'), params).json()

    parseMethod = parse.processAPICallBulk if len(locationNames) > 1 else parse.processAPICall
    return parseMethod(r['data'], locationNames, configurations)