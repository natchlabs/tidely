import datetime
import heapq

def handleAPICall(responseBulk, locationNames, configurations):
    """Apply a set of WeatherConfigurations to a bulk API call and return information suitable for the end-user

    Given the list of responses from the 'data' attribute of a response from the worldweatheronline bulk API, this function
    parses the response and applies a set of WeatherConfigurations to the result to return a list of formatted weather
    chunks which are suitable to be sent to the end-user. Essentially, this turns a collection of weather information for
    multiple locations into a list of activity recommendations for the end-user.
    """

    response = [parseResponse(response[0], response[1]) for response in zip(responseBulk, locationNames)]
        
    # process the response for each location and then flatten it
    output = list(heapq.merge(*(applyConfigurations(l, configurations) for l in response), key=lambda x: x['isoStart']))
    for c in configurations: c.reset()

    return output

def applyConfigurations(response, configurations):
    return list(heapq.merge(*(c(response) for c in configurations), key=lambda x: x['isoStart']))

def parseResponse(responseRaw, locationName):
    """Parses the response from the worldweatheronline marine API into a format readable by WeatherConfiguration objects
    
    Returns a flattened list of hourly weather chunks, extracted from the API response. Each hourly weather chunk has
    metadata referring to the location which it represents attached so that this information is not list in the flattening
    process. The return value from this function can be passed to a WeatherConfiguration object to generate
    activity recommendations for a set of locations for a user.
    """
    def createMetadata(day, hourly):
        return {
            'time': hourlyToDatetime(day['date'], hourly['time']),
            'location': locationName,
            'dayWeather': { 'tides': day['tides'], 'astronomy': day['astronomy'] }
        }
        
    return [merge(hourly, createMetadata(day, hourly)) for day in responseRaw['weather'] for hourly in day['hourly']]

def hourlyToDatetime(date, time):
    """Convert the worldweatheronline hourly time format into a python datetime object"""
    d = [int(a) for a in date.split('-')]
    return datetime.datetime(*d, int(int(time) / 100))

def merge(a, b):
    return { **a, **b }