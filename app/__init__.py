from flask import Flask
from flask_cors import CORS, cross_origin

import app.controllers as controllers
import app.weather.filters as filters
from app.locations import nearbyLocations, nzlocations
import app.weather.codes as codes
import calendar
from datetime import datetime

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
    return {
        'chunks': controllers.getWeatherForKnownLocations(locations, configurations),
        'bounds': filters.getBounds(configurations),
        'activities': [configuration.activity for configuration in configurations],
        'locations': [location['name'] for location in locations],
        'days': ['Today', 'Tomorrow'] + [ calendar.day_name[day] for day in calendar.Calendar(datetime.now().day).iterweekdays()][2:]
    }

if __name__ == "__main__":
    app.run()