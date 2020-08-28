from flask import Flask
from flask_cors import CORS, cross_origin

import controllers
from filters import WeatherConfiguration, BoundMatcher

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# example preset WeatherConfigurations for the user who is not logged in
walking = WeatherConfiguration('Walking', [ BoundMatcher('FeelsLikeC', 12, 20), BoundMatcher('precipMM', 0, 0)])
rainCollecting = WeatherConfiguration('Rain collecting', [ BoundMatcher('FeelsLikeC', 0, 13), BoundMatcher('precipMM', 0.01, 10) ])

@app.route('/')
def getRecommendations():
    return { 'chunks': controllers.getWeather(['Orewa', 'Hatfields beach, Auckland'], [ walking, rainCollecting ]) }