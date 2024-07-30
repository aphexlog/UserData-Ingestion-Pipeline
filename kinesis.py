import boto3
import time

stream_name = 'userdata-ingestion-pipeline-dev-stream'
shard_iterator_type = 'TRIM_HORIZON'  # options: AT_SEQUENCE_NUMBER | AFTER_SEQUENCE_NUMBER | TRIM_HORIZON | LATEST | AT_TIMESTAMP

client = boto3.client('kinesis')

# Get the shard ID
response = client.describe_stream(StreamName=stream_name)
shard_id = response['StreamDescription']['Shards'][0]['ShardId']

# Get the shard iterator
shard_iterator = client.get_shard_iterator(StreamName=stream_name,
                                           ShardId=shard_id,
                                           ShardIteratorType=shard_iterator_type)['ShardIterator']

while True:
    records_response = client.get_records(ShardIterator=shard_iterator, Limit=100)
    shard_iterator = records_response['NextShardIterator']

    if records_response['Records']:
        print("Records fetched:")
        for record in records_response['Records']:
            print(record)
    else:
        print("No new records, waiting...")

    time.sleep(5)
