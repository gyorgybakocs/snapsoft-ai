import os
import boto3
import io
import pandas as pd
from processor import CarDataProcessor

# PURPOSE: 
#   Initialize the S3 client outside the handler to take advantage of 
#   Lambda execution environment reuse.
s3_client = boto3.client('s3')

# Only for requirements.txt
# print(f"--- PANDAS VERSION: {pd.__version__} ---")
# print(f"--- BOTO VERSION: {boto3.__version__} ---")

def handler(event, context):
    """
    PURPOSE:
        AWS Lambda entry point for S3-triggered preprocessing.
        Orchestrates the data flow from the landing bucket to the curated bucket.

    WHY:
        Using an event-driven architecture ensures that processing scales 
        automatically with data uploads and decouples the ingestion 
        from the transformation logic.

    TRADE-OFF:
        The function processes one record at a time (index 0). While simple,
        this assumes the S3 trigger is configured with a batch size of 1.
        For very high-frequency uploads, an SQS buffer might be a safer alternative.

    RISKS:
        Heavy CSV files might exceed the 512MB memory limit or the 10s timeout 
        defined in the infrastructure. Large datasets should be handled 
        via AWS Glue or batch jobs.
    """
    try:
        # Configuration is pulled from environment variables to keep the code 
        # agnostic of specific bucket names or environment stages.
        target_bucket = os.environ.get('TARGET_BUCKET')
        target_prefix = os.environ.get('TARGET_PREFIX', 'curated/')
        
        # Extracts event metadata to identify the source object.
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        source_key = record['object']['key']
        
        # Maintains the original filename in the curated zone for 
        # easier traceability and lineage tracking.
        file_name = os.path.basename(source_key)
        target_key = f"{target_prefix}{file_name}"
        
        # 1. Fetch data from landing zone
        # The entire object is read into memory. This is efficient for the 
        # sample dataset size but would require streaming for multi-GB files.
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))
        
        # 2. Execute cleaning via Processor class
        # Business logic is encapsulated in the CarDataProcessor to maintain 
        # a clean separation between the infrastructure handler and data rules.
        processor = CarDataProcessor(df)
        curated_df = processor.run_preprocessing()
        
        # 3. Save result to curated zone
        # The result is converted back to CSV format. 
        # Trade-off: Parquet would be more efficient for querying (Athena), 
        # but CSV is kept here for human readability and simple validation.
        csv_buffer = io.StringIO()
        curated_df.to_csv(csv_buffer, index=False)
        
        s3_client.put_object(
            Bucket=target_bucket,
            Key=target_key,
            Body=csv_buffer.getvalue()
        )
        
        return {'statusCode': 200, 'body': f"Success: {target_key} saved."}
    except Exception as e:
        # Detailed error logging is crucial for debugging serverless 
        # executions where direct access to the environment is not possible.
        print(f"Error: {str(e)}")
        raise e
