import grequests

from dotenv import load_dotenv
load_dotenv()
import os
# add caching and error handling - currently only works if the geocoding is successful
def geocode(names):
    params = { 'key': os.environ.get('location-iq-key'), 'format': 'json', 'limit': 1 }
    rs = grequests.map((grequests.get(os.environ.get('location-iq-url'), params={ **params, **{ 'q': name } }) for name in names))

    # return [{ 'q': location['lat'] + ',' + location['lon'], 'name': location['display_name'] } for r in rs for location in r.json()]
    return [location['lat'] + ',' + location['lon'] for r in rs for location in r.json()]
