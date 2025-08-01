import os
import requests
from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# IMPORTANT: Store your API key in an environment variable for safety
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Define the main route for the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None

    # This block runs when the user submits the form
    if request.method == 'POST':
        city = request.form['city']
        if not API_KEY:
            error_message = "API key is not set. Please set the OPENWEATHER_API_KEY environment variable."
        else:
            # Parameters for the API request
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # Use 'imperial' for Fahrenheit
            }
            # Make the API request
            response = requests.get(API_URL, params=params)
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                # Organize the data we need
                weather_data = {
                    'city': data['name'],
                    'temperature': f"{data['main']['temp']}°C",
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon']
                }
            else:
                # If the city is not found or another error occurs
                error_message = f"Could not find weather data for '{city}'."

    # Render the HTML page, passing in any weather data or error messages
    return render_template('index.html', weather_data=weather_data, error_message=error_message)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)