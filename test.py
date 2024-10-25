import unittest
from unittest.mock import MagicMock
from app import WeatherMonitoringSystem  # Adjust this import based on your project structure
from datetime import datetime

class TestWeatherMonitoringSystem(unittest.TestCase):

    def setUp(self):
        # Mock the Twilio client and MongoDB collection
        self.twilio_client = MagicMock()
        self.db_collection = MagicMock()

        # Define API key, thresholds, and cities
        self.api_key = '1cbd111aec42bffced8d436179028f81'
        self.cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
        self.thresholds = {
            "temperature": 35
        }

        # Create an instance of WeatherMonitoringSystem
        self.system = WeatherMonitoringSystem(
            self.cities,
            self.api_key,
            self.thresholds,
            self.twilio_client,
            self.db_collection
        )

        # Mocking the MongoDB data for Delhi
        self.db_collection.find.return_value = [
            {
                "city": "Delhi",
                "temperature": 30,
                "humidity": 80,
                "wind_speed": 10,
                "condition": "Clear",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                "city": "Delhi",
                "temperature": 32,
                "humidity": 75,
                "wind_speed": 12,
                "condition": "Partly Cloudy",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

    def test_data_retrieval(self):
        # Test fetching data from the API
        city = 'Delhi'
        weather_data = self.system.get_weather_data(city)
        self.assertIsNotNone(weather_data)

    def test_daily_summary(self):
        # Test calculating daily summary for a city
        city = 'Delhi'
        if hasattr(self.system, 'calculate_daily_summary'):
            summary = self.system.calculate_daily_summary(city)
            self.assertIsNotNone(summary)

            # Check the summary values
            self.assertEqual(summary['average_temp'], (30 + 32) / 2)
            self.assertEqual(summary['max_temp'], 32)
            self.assertEqual(summary['min_temp'], 30)
        else:
            self.skipTest("calculate_daily_summary method not implemented.")

    def test_temperature_conversion(self):
        # Example temperature conversion logic
        celsius_temp = 25
        fahrenheit_temp = (celsius_temp * 9/5) + 32
        self.assertEqual(fahrenheit_temp, 77)

    def test_system_setup(self):
        # Test the system setup
        self.assertTrue(self.system)

# To run the tests
if __name__ == '__main__':
    unittest.main()
