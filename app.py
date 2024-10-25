from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from twilio.rest import Client
import logging
from datetime import datetime, timedelta
import time
from threading import Thread
from collections import defaultdict
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_NUMBER')
user_phone_number = os.getenv('RECIPIENT_NUMBER')

# OpenWeatherMap API key from environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['weather_data']
weather_collection = db['daily_summaries']

# Temperature threshold
thresholds = {
    "temperature": 35
}

# Twilio client
client = Client(account_sid, auth_token)

# List of metros in India
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

class WeatherMonitoringSystem:
    def __init__(self, cities, api_key, thresholds, twilio_client, db_collection):
        self.cities = cities
        self.api_key = api_key
        self.thresholds = thresholds
        self.twilio_client = twilio_client
        self.db_collection = db_collection
        self.breach_count = 0

    # Function to fetch weather data from OpenWeatherMap API
    def get_weather_data(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {str(e)}")
            return None

    # Function to send SMS alerts via Twilio
    def send_alert_via_twilio(self, message):
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=user_phone_number
            )
            logging.info("Alert sent!")
        except Exception as e:
            logging.error(f"Failed to send alert: {str(e)}")

    # Check if temperature exceeds threshold and send alert if necessary
    def check_thresholds(self, temperature):
        temp_threshold = self.thresholds["temperature"]

        if temperature > temp_threshold:
            self.breach_count += 1
            message = f"Alert: Temperature exceeded {temp_threshold}°C! Current Temp: {temperature}°C"
            self.send_alert_via_twilio(message)
        else:
            self.breach_count = 0

    # Function to insert weather data into MongoDB
    def insert_weather_data(self, city, main_temp, feels_like_temp, humidity, wind_speed, condition):
        self.db_collection.insert_one({
            "city": city,
            "temperature": main_temp,
            "feels_like": feels_like_temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "condition": condition,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        logging.info(f"Weather data for {city} inserted into MongoDB.")

    # Function to clean up old weather records
    def cleanup_old_data(self):
        cutoff_date = datetime.now() - timedelta(days=5)
        result = self.db_collection.delete_many({"timestamp": {"$lt": cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}})
        logging.info(f"Deleted {result.deleted_count} old weather records.")

    # Function to continuously fetch weather data
    def continuous_weather_fetch(self):
        while True:
            for city in self.cities:
                weather_data = self.get_weather_data(city)

                if weather_data and weather_data.get("cod") == 200:
                    main_temp = weather_data["main"]["temp"]
                    feels_like_temp = weather_data["main"]["feels_like"]
                    humidity = weather_data["main"]["humidity"]
                    wind_speed = weather_data["wind"]["speed"]
                    condition = weather_data["weather"][0]["description"]

                    # Check thresholds and send alert if necessary
                    self.check_thresholds(main_temp)

                    # Insert data into MongoDB
                    self.insert_weather_data(city, main_temp, feels_like_temp, humidity, wind_speed, condition)

            # Clean up old data
            self.cleanup_old_data()

            # Wait 5 minutes before the next fetch
            time.sleep(300)

# Function to calculate daily summary for a specific city
def calculate_daily_summary(city):
    today = datetime.now().strftime('%Y-%m-%d')

    # Fetch all records for the city for today
    weather_data_list = list(weather_collection.find({
        "city": city,
        "timestamp": {"$regex": f"^{today}"}  # Match records starting with today's date
    }))
    
    if not weather_data_list:
        return {"message": f"No weather data available for {city} on {today}."}  # Handle no data case
    
    # Initialize variables for summary calculations
    total_temp = 0
    total_humidity = 0
    total_wind_speed = 0
    conditions_count = defaultdict(int)
    max_temp = float('-inf')
    min_temp = float('inf')

    # Process each data entry for the city
    for data in weather_data_list:
        temp = data.get('temperature', 0)
        humidity = data.get('humidity', 0)
        wind_speed = data.get('wind_speed', 0)
        condition = data.get('condition', "unknown")

        # Accumulate values
        total_temp += temp
        total_humidity += humidity
        total_wind_speed += wind_speed
        max_temp = max(max_temp, temp)
        min_temp = min(min_temp, temp)
        conditions_count[condition] += 1

    # Calculate averages
    record_count = len(weather_data_list)
    average_temp = total_temp / record_count
    average_humidity = total_humidity / record_count
    average_wind_speed = total_wind_speed / record_count
    dominant_condition = max(conditions_count, key=conditions_count.get)
    
    reason = f"The dominant weather condition for {city} is '{dominant_condition}' because it occurred {conditions_count[dominant_condition]} times today."

    # Summary record structure
    summary_record = {
        "city": city,
        "date": today,
        "average_temp": round(average_temp, 2),
        "max_temp": round(max_temp, 2),
        "min_temp": round(min_temp, 2),
        "average_humidity": round(average_humidity, 2),
        "average_wind_speed": round(average_wind_speed, 2),
        "dominant_condition": dominant_condition,
        "reason": reason
    }

    # Store summary in MongoDB for future reference
    weather_collection.update_one(
        {"city": city, "date": today},
        {"$set": summary_record},
        upsert=True
    )

    return summary_record

# Flask route to fetch weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    weather_system = WeatherMonitoringSystem(cities, API_KEY, thresholds, client, weather_collection)
    weather_data = weather_system.get_weather_data(city)
    return jsonify(weather_data)

# Flask route to fetch daily summary for a specific city
@app.route('/daily-summary', methods=['GET'])
def get_daily_summary():
    city = request.args.get('city')
    if not city or city not in cities:
        return jsonify({"error": "City not specified or not supported."}), 400
    daily_summary = calculate_daily_summary(city)
    return jsonify(daily_summary)

# Main route to display home page
@app.route('/')
def index():
    return render_template('index.html')

# Create an instance of the WeatherMonitoringSystem class
weather_system = WeatherMonitoringSystem(cities, API_KEY, thresholds, client, weather_collection)

# Start continuous weather fetching in a background thread
weather_fetch_thread = Thread(target=weather_system.continuous_weather_fetch)
weather_fetch_thread.daemon = True
weather_fetch_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
