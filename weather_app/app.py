from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your API key from OpenWeatherMap
API_KEY = 'place your api key'

# Base URL for the OpenWeatherMap API
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Default city to show weather information
DEFAULT_CITY = 'New York'

def get_weather(city):
    try:
        # Make an API call to OpenWeatherMap
        params = {
            'q': city,
            'units': 'metric',
            'appid': API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        weather_data = response.json()

        # Extract relevant weather information
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        city_name = weather_data['name']

        return {
            'city': city_name,
            'temperature': temperature,
            'description': description
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = DEFAULT_CITY
    
    weather_info = get_weather(city)
    
    return render_template('index.html', weather=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
