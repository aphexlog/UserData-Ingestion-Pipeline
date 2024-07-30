import json
import boto3
from os import environ
from mypy_boto3_s3 import S3Client
from aws_lambda_powertools import Logger
import base64

logger = Logger(service="consumer")

s3_client: S3Client = boto3.client("s3")  # type: ignore

def lambda_handler(event, context):
    payload = None
    for record in event["Records"]:
        try:
            # Decode the base64-encoded data and convert to JSON
            payload = json.loads(base64.b64decode(record["kinesis"]["data"]).decode('utf-8'))
            logger.info(f"Decoded payload: {payload}")

            # Filter data based on age
            if payload.get("age", 0) > 21:
                file_name = f"{payload.get('first_name', 'unknown')}_{payload.get('last_name', 'unknown')}.json"
                s3_client.put_object(
                    Bucket=environ["S3_BUCKET_NAME"],
                    Key=file_name,
                    Body=json.dumps(payload)  # Convert payload back to JSON string before storing
                )
                logger.info(f"Data stored in S3: {payload}")

        except (json.JSONDecodeError, KeyError):
            logger.exception(f"Error decoding payload: {payload}")
            continue

    return {
        "statusCode": 200,
        "body": json.dumps("Data processed and stored successfully")
    }

if __name__ == "__main__":
    lambda_handler(None, None)
