from flask import Flask
from flask_cors import CORS, cross_origin

import controllers
from filters import BoundMatcher, TideMatcher, TimeMatcher, TimeMatcher, WeatherCodeMatcher, WeatherConfiguration
from locations import nearbyLocations, nzlocations
import codes

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# example preset WeatherConfigurations for the user who is not logged in
walking = WeatherConfiguration('Walking', [ WeatherCodeMatcher(codes.calm) ])
rainCollecting = WeatherConfiguration('Rain collecting', [ WeatherCodeMatcher(codes.raining) ])

@app.route('/<lat>,<lng>')
def getNearbyRecommendations(lat, lng):
    lat, lng = float(lat), float(lng)
    locations = nearbyLocations({ 'lat': lat, 'lng': lng }, nzlocations, 5)
    return { 'chunks': controllers.getWeatherForKnownLocations(locations, [ walking, rainCollecting ]) }

if __name__ == "__main__":
    app.run()