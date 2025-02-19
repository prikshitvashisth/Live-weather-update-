import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "9e54e95c58ee629d0c66ba20c5d87993"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # Default units: Celsius

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    

    scale = request.form.get('scale', 'metric')
    

    global UNITS
    UNITS = scale
    
    weather_data = fetch_weather_data(city)
    return render_template('index.html', weather_data=weather_data, city=city)

def fetch_weather_data(city):
    params = {
        'q': city,
        'units': UNITS,
        'appid': API_KEY,
    }
    response = requests.get(WEATHER_API_URL, params=params)
    print(response.url) 
    if response.status_code == 200:
        data = response.json()
        return {
            'location': data['name'],
            'temperature': f"{data['main']['temp']}°C" if UNITS == 'metric' else f"{data['main']['temp']}°F",
            'description': data['weather'][0]['description'].capitalize(),
        }
    else:
        return {
            'location': 'N/A',
            'temperature': 'N/A',
            'description': 'N/A',
        }

if __name__ == '__main__':
    app.run(debug=True)
