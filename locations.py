import requests
from functools import partial
import json

from dotenv import load_dotenv
load_dotenv()
import os
# add caching and error handling - currently only works if the geocoding is successful
params = { 'key': os.environ.get('geocode-key'), 'thumbMaps': False }
def geocode(names):
    """Take a list of location names and return a list of latitudes and longitudes
    
    If the location cannot be found, 'undefined location' is returned instead. Better error handling will
    be implemented in the future.
    """

    def format(r):
        return str(r['lat']) + ',' + str(r['lng']) if 'lat' in r and 'lng' in r else 'Undefined location'

    body = { 'locations': names } # the body of the request to the geocoding api
    r = requests.post(os.environ.get('geocode-url'), json=body, params=params).json()

    return [format(result['locations'][0]['latLng']) for result in r['results']]
def distance(p1, p2):
    return (p1['lat'] - p2['lat']) ** 2 + (p1['lng'] - p2['lng']) ** 2

def nearbyLocations(p, points, n):
    s = sorted(points, key=partial(distance, p))

    return list(map(lambda l: l['name'], s[0:n]))

with open('nzlocations.json') as f:
    nzlocations = json.load(f)