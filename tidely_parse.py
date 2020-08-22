import datetime
import functools

# replace this with a bijective map and use a database
locations = { '-36.59,174.68': 'Orewa' }

def processAPICall(responseRaw, configurations):
    """Parses the response from the API call with parseResponse and then processes the result with the configurations given."""
    response = parseResponse(responseRaw)
    # using lists may be inefficient here
    elements = functools.reduce(lambda acc,cur: cur(response) + acc, configurations, [])
    return elements

def parseResponse(responseRaw):
    """parses the response from the API call into a list of chunks which each have metadata attached."""
    def createMetadata(day, hourly):
        return {
            'time': toDatetime(day['date'], hourly['time']),
            'location': parseLocation(responseRaw)
        }
    return [merge(hourly, createMetadata(day, hourly)) for day in responseRaw['data']['weather'] for hourly in day['hourly']]

def parseLocation(response):
    """Parses the latitude and longitude from the API call and uses a cache to reverse-geocode it to be used as metadata"""
    raw = response['data']['request'][0]['query']
    parsed = ','.join([elem[4:] for elem in raw.split(' and ')])
    return locations[parsed]

LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

def toDatetime(date, time):
    d = [int(a) for a in date.split('-')]
    return datetime.datetime(*d, int(int(time) / 100), tzinfo=LOCAL_TIMEZONE)

def merge(a, b):
    return { **a, **b }