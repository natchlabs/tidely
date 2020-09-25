from flask import Flask
from flask_cors import CORS, cross_origin

import controllers
import filters
from locations import nearbyLocations, nzlocations
import codes

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# example preset WeatherConfigurations for the user who is not logged in
walking = filters.WeatherConfiguration('Walking', [ filters.WeatherCodeMatcher(codes.calm), filters.TimeMatcher(5, 22) ])
rainCollecting = filters.WeatherConfiguration('Rain collecting', [ filters.WeatherCodeMatcher(codes.raining), filters.TimeMatcher(5, 22) ])

@app.route('/<lat>,<lng>')
def getNearbyRecommendations(lat, lng):
    lat, lng = float(lat), float(lng)
    locations = nearbyLocations({ 'lat': lat, 'lng': lng }, nzlocations, 5)

    configurations = [ rainCollecting, walking ]
    return { 'chunks': controllers.getWeatherForKnownLocations(locations, configurations), 'bounds': filters.getBounds(configurations) }

if __name__ == "__main__":
    app.run()