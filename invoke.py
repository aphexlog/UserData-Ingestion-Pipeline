import boto3
from mypy_boto3_lambda import LambdaClient

lambda_client: LambdaClient = boto3.client('lambda') # type: ignore

count = 0
while True:
    try:
        count += 1
        response = lambda_client.invoke(
            FunctionName='userdata-ingestion-pipeline-dev-producer',
            InvocationType='RequestResponse',
            Payload=b'{}'
        )
        print(f"Invocation count: {count}")
    except Exception as e:
        print(f"An error occurred: {e}")
