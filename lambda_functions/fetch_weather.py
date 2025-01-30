import os
import json
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    city = event.get('city')
    api_key = os.getenv('OPENWEATHER_API_KEY')

    logger.info(f"Fetching weather for {city}...")

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "imperial"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        logger.info(f"Successfully fetched weather data for {city}")
        return {'statusCode': 200, 'body': json.dumps(weather_data)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data for {city}: {e}")
        return {'statusCode': 500, 'body': str(e)}
