from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
API_KEY = '5225ce26df391f8a25a2433215881d84'  # Replace with your OpenWeatherMap API key

# Map weather descriptions to image filenames
WEATHER_IMAGES = {
    'clear sky': 'sunny.png',
    'few clouds': 'cloudy.png',
    'scattered clouds': 'cloudy.png',
    'broken clouds': 'cloudy.png',
    'shower rain': 'rainy.png',
    'rain': 'rainy.png',
    'thunderstorm': 'stormy.png',
    'snow': 'snowy.png',
    'mist': 'cloudy.png',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'No city provided'}), 400

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        city_name = data['name']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        # Map description to image filename
        image_filename = WEATHER_IMAGES.get(description, 'default.png')
        image_url = f'/static/images/{image_filename}'
        
        # Mock historical data for the chart
        temperature_history = [
            {'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'), 'temperature': temperature - i}
            for i in range(7)
        ]
        
        return jsonify({
            'city': city_name,
            'temperature': temperature,
            'description': description,
            'image': image_url,
            'pressure': pressure,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'temperatureHistory': temperature_history
        })
    else:
        return jsonify({'error': 'City not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)




