import app.weather.parse as parse
from app.weather.filters import WeatherMatcher, WeatherConfiguration
from app.locations import geocode
import app.weather.cache as cache

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

    r = cache.requestWeatherInformation(locations)
    return parse.handleAPICall(r, [l['name'] for l in locations], configurations)