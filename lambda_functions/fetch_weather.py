import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event, context):
    city = event.get('city')
    api_key = os.getenv('OPENWEATHER_API_KEY')

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
        return {
            'statusCode': 200,
            'body': json.dumps(weather_data)
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }