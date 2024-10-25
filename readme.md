# Weather Monitoring System

## Overview

A Flask-based web application that provides real-time weather monitoring and alerts for major Indian cities. The system fetches data from the OpenWeatherMap API, stores it in MongoDB, and sends SMS alerts via Twilio when temperature thresholds are exceeded.

## Features

- **Real-time Weather Monitoring**: Fetches weather data every 5 minutes for Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad.
- **Interactive Dashboard**: User-friendly web interface showing current weather conditions and daily summaries.
- **SMS Alerts**: Automated alerts via Twilio when temperature thresholds are exceeded.
- **Data Persistence**: Stores weather data in MongoDB for historical analysis.
- **Daily Weather Summary**: Provides aggregated weather data including:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition
  - Humidity and wind speed averages

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: OpenWeatherMap API, Twilio API
- **Additional Libraries**:
  - `requests`
  - `pymongo`
  - `twilio`
  - `python-dotenv`

## Prerequisites

- Python 3.7+
- MongoDB
- OpenWeatherMap API key
- Twilio account credentials

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd weather-monitoring-system
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the root directory with your credentials:**

   ```plaintext
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_NUMBER=your_twilio_phone_number
   RECIPIENT_NUMBER=your_recipient_phone_number
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   ```

## Usage

1. **Start the application:**

   ```bash
   python app.py
   ```

2. **Access the web interface at** `http://localhost:5000`

   - Enter a city name to get current weather information.
   - View daily summaries and metro city weather data.

## API Endpoints

- `/weather?city={city_name}`: Get current weather data for a specific city.
- `/daily-summary?city={city_name}`: Get daily weather summary for a specific city.

## Testing

Run the test suite:

```bash
python -m unittest test.py
```

## Project Structure

```plaintext
weather-monitoring-system/
├── app.py              # Main application file
├── test.py             # Test suite
├── requirements.txt    # Project dependencies
├── .env                # Environment variables
└── templates/
    └── index.html      # Web interface template
```

## Features in Detail

### Weather Data Collection
- Fetches weather data every 5 minutes.
- Stores temperature, humidity, wind speed, and weather conditions.
- Automatically cleans up data older than 5 days.

### Alert System
- Monitors temperature thresholds.
- Sends SMS alerts when temperature exceeds configured threshold.
- Tracks consecutive threshold breaches.

### Daily Summaries
- Calculates average, maximum, and minimum temperatures.
- Determines dominant weather conditions.
- Provides detailed weather analysis for each city.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.

## Acknowledgments

- OpenWeatherMap API for weather data
- Twilio for SMS functionality
- MongoDB for database services
