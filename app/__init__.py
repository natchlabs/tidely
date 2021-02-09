import calendar
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

import app.controllers as controllers
import app.weather.codes as codes
import app.weather.filters as filters

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# example preset WeatherConfigurations for the user who is not logged in
walking = filters.WeatherConfiguration('Walking', [ filters.WeatherCodeMatcher(codes.calm), filters.TimeMatcher(5, 22) ])
rainCollecting = filters.WeatherConfiguration('Rain collecting', [ filters.WeatherCodeMatcher(codes.raining), filters.TimeMatcher(5, 22) ])

@app.route('/',  methods=['POST'])
def getRecommendations():
    locations = [{
        'name': data['activity'],
        'lat': float(data['location']['lat']),
        'lng': float(data['location']['lng'])
    } for data in request.json]

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