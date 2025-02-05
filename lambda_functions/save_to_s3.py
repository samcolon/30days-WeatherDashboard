import os
import json
import boto3
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def create_bucket_if_not_exists(bucket_name):
    """Create S3 bucket if it doesn't exist"""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} already exists.")
    except:
        logger.info(f"Creating bucket {bucket_name}...")
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            logger.info(f"Successfully created bucket {bucket_name}.")
        except Exception as e:
            logger.error(f"Error creating bucket: {e}")
            return False
    return True

def lambda_handler(event, context):
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    weather_data = json.loads(event.get('weather_data', '{}'))
    city = event.get('city')

    if not weather_data or not city:
        logger.error("Invalid input")
        return {'statusCode': 400, 'body': 'Invalid input'}

    if not create_bucket_if_not_exists(bucket_name):
        logger.error(f"Failed to create S3 bucket: {bucket_name}")
        return {'statusCode': 500, 'body': 'Failed to create S3 bucket'}

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    file_name = f"weather-data/{city}-{timestamp}.json"

    try:
        weather_data['timestamp'] = timestamp
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(weather_data),
            ContentType='application/json'
        )
        logger.info(f"Successfully saved data for {city} to S3: {file_name}")
        return {'statusCode': 200, 'body': f"Data saved to {file_name}"}
    except Exception as e:
        logger.error(f"Error saving data to S3: {e}")
        return {'statusCode': 500, 'body': str(e)}

