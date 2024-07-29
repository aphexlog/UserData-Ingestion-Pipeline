import json
import boto3
from os import environ
from mypy_boto3_s3 import S3Client
from aws_lambda_powertools import Logger

logger: Logger = Logger(service="consumer")

s3_client: S3Client = boto3.client("s3") # type: ignore

def lambda_handler(event, context):
    for record in event["Records"]:
        payload = json.loads(record["kinesis"]["data"])

        # Filter data based on age
        if payload["age"] > 21:
            file_name = f"{payload['first_name']}_{payload['last_name']}.json"
            s3_client.put_object(
                Bucket=environ["S3_BUCKET_NAME"],
                Key=file_name,
                Body=json.dumps(payload)
            )
            logger.info(f"Data stored in S3: {payload}")

    return {
        "statusCode": 200,
        "body": json.dumps("Data processed and stored successfully")
    }
