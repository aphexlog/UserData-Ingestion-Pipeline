import json
import boto3
import requests
from botocore import exceptions
from mypy_boto3_kinesis import KinesisClient
from aws_lambda_powertools import Logger
from os import environ

logger: Logger = Logger(service="producer")

kinesis_client: KinesisClient = boto3.client('kinesis') # type: ignore

def lambda_handler(event, context):
    response = requests.get('https://randomuser.me/api/')
    user_data = response.json()['results'][0]

    # Prepare the record to be sent to the Kinesis stream
    data = {
        'user': user_data['name']['first'],
        'email': user_data['name']['last'],
        'age': user_data['dob']['age'],
        'gender': user_data['gender'],
        'latitude': user_data['location']['coordinates']['latitude'],
        'longitude': user_data['location']['coordinates']['longitude']
    }

    logger.info(f"User data: {data}")

    # Send the record to the Kinesis stream
    try:
        kinesis_client.put_record(
            StreamName=environ['KINESIS_STREAM_NAME'],
            Data=json.dumps(data),
            PartitionKey='1'
        )
    except exceptions.ClientError:
        logger.exception("Error sending user data to Kinesis stream")

    return {
        'statusCode': 200,
        'body': json.dumps('User data sent to Kinesis stream')
    }

if __name__ == "__main__":
    lambda_handler(None, None)
