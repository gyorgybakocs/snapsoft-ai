import os
import boto3
import io
import pandas as pd
from processor import CarDataProcessor

s3_client = boto3.client('s3')

def handler(event, context):
    try:
        target_bucket = os.environ.get('TARGET_BUCKET')
        target_prefix = os.environ.get('TARGET_PREFIX', 'curated/')
        
        record = event['Records'][0]['s3']
        source_bucket = record['bucket']['name']
        source_key = record['object']['key']
        
        file_name = os.path.basename(source_key)
        target_key = f"{target_prefix}{file_name}"
        
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        df = pd.read_csv(io.BytesIO(response['Body'].read()))
        
        processor = CarDataProcessor(df)
        curated_df = processor.run_preprocessing()
        
        csv_buffer = io.StringIO()
        curated_df.to_csv(csv_buffer, index=False)
        
        s3_client.put_object(
            Bucket=target_bucket,
            Key=target_key,
            Body=csv_buffer.getvalue()
        )
        
        return {'statusCode': 200, 'body': f"Success: {target_key} saved."}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
