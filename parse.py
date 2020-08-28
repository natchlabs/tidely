import datetime
import functools

def handleAPICallBulk(responseBulk, locationNames, configurations):
    """Apply a set of WeatherConfigurations to a bulk API call and return information suitable for the end-user

    Given the 'data' attribute of a response from the worldweatheronline bulk API, this function
    parses the response and applies a set of WeatherConfigurations to the result to return a list of formatted weather
    chunks which are suitable to be sent to the end-user. Essentially, this turns a collection of weather information for
    multiple locations into a list of activity recommendations for the end-user.
    """

    response = parseResponseBulk(responseBulk, locationNames)
    def process(x):
        return functools.reduce(lambda acc,cur: cur(x) + acc, configurations, [])
    # process the response for each location and then flatten it
    return [chunk for locationResponse in response for chunk in process(locationResponse)]


def handleAPICall(responseRaw, locationName, configurations):
    """Apply a set of WeatherConfigurations to a marine API call and return information suitable for the end-user

    This function serves the same purpose as the bulk handling function, but for a single location. This is useful
    because the result of the bulk API call is an array of objects in the same format as the single API call, meaning
    that the bulk function can delegate to this function. Additionally, if only one location is specified in a bulk API
    call, the result is returned in the same format as the single API. In these cases, this function is used.
    """

    response = parseResponse(responseRaw, locationName)
    # using lists may be inefficient here
    elements = functools.reduce(lambda acc,cur: cur(response) + acc, configurations, [])
    return elements


def parseResponseBulk(responseBulk, locationNames):
    """Parse a response from the worldweatheronline bulk API into a format readable by WeatherConfiguration objects

    Returns a flattened list of hourly weather chunks, extracted from the API response. Each hourly weather chunk has
    metadata referring to the location which it represents attached so that this information is not list in the flattening
    process. The return value from this function can be passed to a WeatherConfiguration object to generate
    activity recommendations for a set of locations for a user.
    """
    
    return [parseResponse(response[0], response[1]) for response in zip(responseBulk['area'], locationNames)]

def parseResponse(responseRaw, locationName):
    """Parses the response from the worldweatheronline marine API into a format readable by WeatherConfiguration objects
    
    This function has the exact same purpose and functionality as the bulk version. This function applies to single locations
    and is delegated to by the bulk function.
    """
    def createMetadata(day, hourly):
        return {
            'time': toDatetime(day['date'], hourly['time']),
            'location': locationName
        }
    return [merge(hourly, createMetadata(day, hourly)) for day in responseRaw['weather'] for hourly in day['hourly']]
# get the timezone so that date calculations can be done. This should later be replaced with the user's timezone for a given call
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

def toDatetime(date, time):
    """Convert the worldweatheronline time format into a python datetime object"""
    d = [int(a) for a in date.split('-')]
    return datetime.datetime(*d, int(int(time) / 100), tzinfo=LOCAL_TIMEZONE)

def merge(a, b):
    return { **a, **b }