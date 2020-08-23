from flask import Flask

import weather
from weather_matcher import WeatherConfiguration, WeatherMatcher

app = Flask(__name__)

walking = WeatherConfiguration('Walking', [ WeatherMatcher('FeelsLikeC', 12, 20), WeatherMatcher('precipMM', 0, 0) ])
rainCollecting = WeatherConfiguration('Rain collecting', [ WeatherMatcher('FeelsLikeC', 0, 13), WeatherMatcher('precipMM', 0.01, 10) ])

@app.route('/')
def weatherInformation():
    return { 'chunks': weather.getWeather(['Orewa', 'Hatfields beach, Auckland'], [ walking, rainCollecting ]) }