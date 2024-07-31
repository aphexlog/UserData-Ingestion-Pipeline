# AWS Kinesis Data Stream Project

## Project Description

The goal of this project is to create a data pipeline using AWS services. The pipeline will fetch random user data from an external API, process this data, and store it in an S3 bucket if it meets certain criteria. This project utilizes AWS Kinesis Data Streams for data ingestion and processing, AWS Lambda functions for fetching and processing data, and S3 for data storage.

## Project Summary

1. **Kinesis Data Stream**: Acts as the data ingestion and processing pipeline.
2. **Lambda Function 1**: Fetches data from the Random User API and puts it into the Kinesis Data Stream.
3. **Lambda Function 2**: Processes the data from the Kinesis Data Stream, filters it, and stores relevant information in an S3 bucket.
4. **S3 Bucket**: Stores the processed data in JSON format.

## Task List

### Step 1: Set Up IAM Roles

- [ ] Create IAM role for Lambda functions with permissions to interact with Kinesis Data Streams and S3.
- [ ] Attach the necessary policies to the IAM roles.

### Step 2: Create a Kinesis Data Stream

- [ ] Navigate to the Kinesis service in the AWS Management Console.
- [ ] Create a new Kinesis Data Stream named `RandomUserStream` with the desired shard count.

### Step 3: Create Lambda Function 1 (Data Ingestion)

- [ ] Navigate to the Lambda service in the AWS Management Console.
- [ ] Create a new Lambda function named `IngestRandomUserData`.
- [ ] Use the provided Python code for the Lambda function.
- [ ] Configure the Lambda function with the appropriate execution role.
- [ ] Set up a trigger to run this Lambda function periodically (e.g., using EventBridge or a scheduled CloudWatch event).

### Step 4: Create Lambda Function 2 (Data Processing)

- [ ] Navigate to the Lambda service in the AWS Management Console.
- [ ] Create another Lambda function named `ProcessUserData`.
- [ ] Use the provided Python code for this Lambda function.
- [ ] Configure the Lambda function with the appropriate execution role.
- [ ] Add the Kinesis Data Stream as the trigger for this Lambda function.

### Step 5: Create an S3 Bucket

- [ ] Navigate to the S3 service in the AWS Management Console.
- [ ] Create a new bucket named `random-user-data-bucket`.

### Step 6: Test the Setup

- [ ] Manually trigger the first Lambda function to ingest data.
- [ ] Verify that the data is being processed by the second Lambda function.
- [ ] Check the S3 bucket to ensure the data is stored correctly.

### Additional Considerations

- [ ] Set up monitoring and logging for both Lambda functions using CloudWatch.
- [ ] Implement error handling and retries in Lambda functions for robustness.
- [ ] Ensure that IAM roles have the least privilege necessary to perform their tasks.

## Python Code for Lambda Functions

### IngestRandomUserData

```python
import json
import boto3
import requests

kinesis_client = boto3.client('kinesis')

def lambda_handler(event, context):
    response = requests.get('https://randomuser.me/api/')
    user_data = response.json()['results'][0]

    # Prepare data to send to Kinesis
    data = {
        'first_name': user_data['name']['first'],
        'last_name': user_data['name']['last'],
        'age': user_data['dob']['age'],
        'gender': user_data['gender'],
        'latitude': user_data['location']['coordinates']['latitude'],
        'longitude': user_data['location']['coordinates']['longitude']
    }

    kinesis_client.put_record(
        StreamName='RandomUserStream',
        Data=json.dumps(data),
        PartitionKey='partitionkey'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Data ingested successfully')
    }
```

### ProcessUserData

```python
import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])

        # Filter data based on age
        if payload['age'] >= 21:
            file_name = f"{payload['first_name']}_{payload['last_name']}.json"
            s3_client.put_object(
                Bucket='your-s3-bucket-name',
                Key=file_name,
                Body=json.dumps(payload)
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and stored successfully')
    }
```

### Conclusion

This project provides a practical example of how to integrate various AWS services to create a robust data pipeline. By following this exercise, you will gain hands-on experience with AWS Kinesis Data Streams, Lambda functions, and S3, and learn how to implement data ingestion, processing, and storage workflows in a scalable and efficient manner.
