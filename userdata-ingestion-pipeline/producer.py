import json
import boto3
import requests
import uuid
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger
from os import environ

logger = Logger(service="producer")

kinesis_client = boto3.client('kinesis')

def lambda_handler(event, context):
    try:
        response = requests.get('https://randomuser.me/api/')
        response.raise_for_status()
        user_data = response.json()['results'][0]

        # Prepare the record to be sent to the Kinesis stream
        data = {
            'first_name': user_data['name']['first'],
            'last_name': user_data['name']['last'],
            'email': user_data['email'],
            'age': user_data['dob']['age'],
            'gender': user_data['gender'],
            'latitude': user_data['location']['coordinates']['latitude'],
            'longitude': user_data['location']['coordinates']['longitude']
        }

        logger.info(f"User data: {data}")

        # Generate a random UUID for the partition key
        partition_key = str(uuid.uuid4())

        # Encode the data to JSON string and then to bytes
        encoded_data = json.dumps(data).encode('utf-8')

        # Send the record to the Kinesis stream
        response = kinesis_client.put_record(
            StreamName=environ['KINESIS_STREAM_NAME'],
            Data=encoded_data,
            PartitionKey=partition_key
        )

        logger.info(f"Kinesis put_record response: {response}")

    except ClientError:
        logger.exception("ClientError: Error sending user data to Kinesis stream")
    except requests.RequestException:
        logger.exception("RequestException: Error fetching data from Random User API")
    except Exception:
        logger.exception("Exception: An error occurred")

    return {
        'statusCode': 200,
        'body': json.dumps('User data sent to Kinesis stream')
    }

if __name__ == "__main__":
    lambda_handler(None, None)
