
# Weather Monitoring System

## Overview

The Weather Monitoring System is a Flask-based web application that fetches real-time weather data from the OpenWeatherMap API and sends alerts via Twilio when temperature thresholds are exceeded. The application also stores weather data in a MongoDB database and provides daily summaries for selected cities.

## Features

- **Real-time Weather Data Fetching**: Continuously retrieves weather data for Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad from the OpenWeatherMap API every 5 minutes.
- **Temperature Conversion**: Converts temperature values from Kelvin to Celsius based on user preferences.
- **Daily Weather Summary**: Rolls up daily weather data to calculate:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition (determined based on the frequency of different weather types recorded throughout the day)
- **User-configurable Alerting Thresholds**: Users can set temperature or weather condition thresholds to receive alerts if specific criteria are met (e.g., temperature exceeding 35 degrees Celsius for two consecutive updates).
- **SMS Alerts via Twilio**: Sends SMS alerts for temperature breaches using Twilio, ensuring users are notified promptly.
- **Data Storage**: Stores daily weather summaries and real-time updates in a MongoDB database for persistent storage and analysis.
- **Visualizations**: Displays daily weather summaries, historical trends, and triggered alerts through a user-friendly web interface built with HTML, CSS, and JavaScript.

## Technologies Used

- **Backend**: Flask, Python
- **Database**: MongoDB
- **APIs**: OpenWeatherMap API, Twilio API
- **Frontend**: HTML, CSS, JavaScript

## Data Source

The system will continuously retrieve weather data from the OpenWeatherMap API. You will need to sign up for a free API key to access the data. The API provides various weather parameters, focusing on:

- **Main**: Main weather condition (e.g., Rain, Snow, Clear)
- **Temp**: Current temperature in Celsius
- **Feels Like**: Perceived temperature in Celsius
- **DT**: Time of the data update (Unix timestamp)

## Processing and Analysis

- The system should call the OpenWeatherMap API at a configurable interval (e.g., every 5 minutes) to retrieve real-time weather data for the specified metros.
- For each received weather update:
  - Convert temperature values from Kelvin to Celsius based on user preference.

## Rollups and Aggregates

1. **Daily Weather Summary**:
   - Roll up the weather data for each day.
   - Calculate daily aggregates for:
     - Average temperature
     - Maximum temperature
     - Minimum temperature
     - Dominant weather condition (based on the most frequently occurring weather type throughout the day)
   - Store the daily summaries in a database or persistent storage for further analysis.

2. **Alerting Thresholds**:
   - Define user-configurable thresholds for temperature or specific weather conditions (e.g., alert if the temperature exceeds 35 degrees Celsius for two consecutive updates).
   - Continuously track the latest weather data and compare it with the thresholds.
   - If a threshold is breached, trigger an alert for the current weather conditions. Alerts could be displayed on the console or sent through an email notification system (implementation details left open-ended).

3. **Implement Visualizations**:
   - To display daily weather summaries, historical trends, and triggered alerts, enhancing the user experience and providing valuable insights.

## Installation

1. Clone the repository:


2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MongoDB database and create a collection named `daily_summaries`.

5. Create a `.env` file in the root of your project and add the following variables:

   ```plaintext
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   MONGODB_URI=your_mongodb_uri
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   USER_PHONE_NUMBER=your_user_phone_number
   ```

6. Replace the placeholders with your actual credentials.

## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- Navigate to the homepage to enter a city name and fetch its current weather data.
- The application will display current weather conditions, including temperature, humidity, wind speed, and more.
- Daily summaries can be triggered via the `/daily_summary` endpoint.

## Testing

To run the tests, use the following command:

```bash
python -m unittest test.py
```

### Ensuring Application Runs Correctly

Before deployment, ensure that the application is running correctly by executing the tests and checking the functionality through the browser.

## Non-Functional Requirements

### Security

- **Environment Variables**: Store sensitive information in the `.env` file to secure API keys and credentials.
- **Input Validation**: Implement input validation to prevent injection attacks and ensure data integrity.

### Performance

- **Caching**: Consider implementing caching for frequently accessed data to reduce API calls and improve response times.
- **Asynchronous Requests**: Utilize asynchronous requests for fetching weather data to enhance performance and responsiveness.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for discussion.
