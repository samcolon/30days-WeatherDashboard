import os
import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    weather_data = json.loads(event.get('weather_data', '{}'))
    city = event.get('city')

    if not weather_data or not city:
        return {'statusCode': 400, 'body': 'Invalid input'}

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    file_name = f"weather-data/{city}-{timestamp}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(weather_data),
            ContentType='application/json'
        )
        return {'statusCode': 200, 'body': f"Data saved to {file_name}"}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}