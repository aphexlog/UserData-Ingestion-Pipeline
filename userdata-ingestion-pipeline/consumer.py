import json
import boto3
from os import environ

s3_client = boto3.client("s3")

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

    return {
        "statusCode": 200,
        "body": json.dumps("Data processed and stored successfully")
    }
