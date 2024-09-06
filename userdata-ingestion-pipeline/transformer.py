import base64
from aws_lambda_powertools import Logger

logger: Logger = Logger(service="invoke")

def lambda_handler(event, context):
    logger.info("Invoking transformer lambda")

    # Process each record in the event
    output = []
    for record in event['records']:
        # Perform "identity" transformation (no actual change)
        record_id = record['recordId']
        base64_data = base64.b64decode(record['data']).decode('utf-8')

        # Append a newline character to ensure each record is on a new line
        new_data = base64_data + "\n"

        transformed_record = {
            'recordId': record_id,
            'result': 'Ok',
            'data': base64.b64encode(new_data.encode('utf-8')).decode('utf-8')
        }
        output.append(transformed_record)

    logger.info(f"Processing completed. Successful records: {len(output)}.")

    # Return transformed records
    return {
        'records': output
    }
