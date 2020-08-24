from flask import Flask

import controllers
from filters import WeatherConfiguration, WeatherMatcher

app = Flask(__name__)

# example preset WeatherConfigurations for the user who is not logged in
walking = WeatherConfiguration('Walking', [ WeatherMatcher('FeelsLikeC', 12, 20), WeatherMatcher('precipMM', 0, 0) ])
rainCollecting = WeatherConfiguration('Rain collecting', [ WeatherMatcher('FeelsLikeC', 0, 13), WeatherMatcher('precipMM', 0.01, 10) ])

@app.route('/')
def getRecommendations():
    return { 'chunks': controllers.getWeather(['Orewa', 'Hatfields beach, Auckland'], [ walking, rainCollecting ]) }
    