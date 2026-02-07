import sys
import os
import json
import boto3
import pytest
from moto import mock_aws

# Add lambda directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../lambda'))

from handler import handler

@pytest.fixture
def s3_event():
    """
    Simulates a typical S3 Event JSON structure sent by AWS to Lambda.
    """
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "test-landing-bucket"
                    },
                    "object": {
                        "key": "input/test_car.csv"
                    }
                }
            }
        ]
    }

@mock_aws
def test_handler_end_to_end(s3_event, monkeypatch):
    """
    End-to-End test simulating the full pipeline using in-memory S3 (moto).
    """
    # 1. Set environment variables (simulating Terraform outputs)
    monkeypatch.setenv("TARGET_BUCKET", "test-curated-bucket")
    monkeypatch.setenv("TARGET_PREFIX", "curated/")
    # IMPORTANT: Set AWS region for the mock
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-central-1")

    # 2. Create mock S3 buckets
    s3 = boto3.client("s3", region_name="eu-central-1")
    s3.create_bucket(
        Bucket="test-landing-bucket",
        CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'}
    )
    s3.create_bucket(
        Bucket="test-curated-bucket",
        CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'}
    )

    # 3. Upload test CSV to landing bucket
    csv_content = """car_ID,CarName,Price,ownername,carbody,fueltype,doornumber
1,toyouta corolla,15000,John Doe,sedan,gas,four"""
    
    s3.put_object(
        Bucket="test-landing-bucket",
        Key="input/test_car.csv",
        Body=csv_content
    )

    # 4. INVOKE HANDLER
    response = handler(s3_event, None)

    # 5. Assertions
    assert response['statusCode'] == 200
    
    # Verify file exists in curated bucket
    result = s3.list_objects(Bucket="test-curated-bucket", Prefix="curated/")
    assert 'Contents' in result
    assert result['Contents'][0]['Key'] == "curated/test_car.csv"

    # Verify content transformation (PII removal, typo fix)
    processed_obj = s3.get_object(Bucket="test-curated-bucket", Key="curated/test_car.csv")
    processed_csv = processed_obj['Body'].read().decode('utf-8')
    
    # Check: Was 'toyouta' fixed to 'toyota'?
    assert "toyota" in processed_csv
    # Check: Was 'ownername' (PII) removed?
    assert "John Doe" not in processed_csv

@mock_aws
def test_handler_error_propagation(s3_event, monkeypatch, capsys):
    """
    Test scenario where the S3 download fails (e.g., missing bucket).
    Verifies that the handler logs the error and re-raises the exception.
    """
    # 1. Set environment variables (required for boto3 initialization)
    monkeypatch.setenv("TARGET_BUCKET", "test-curated-bucket")
    monkeypatch.setenv("TARGET_PREFIX", "curated/")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-central-1")

    # 2. INTENTIONAL OMISSION: We do NOT create the S3 buckets.
    # Since 'moto' memory is empty, when the handler tries to download
    # the file from 'test-landing-bucket', boto3 will raise an error (NoSuchBucket).

    # 3. Verify that the handler re-raises the exception
    # pytest.raises catches the error, making the test pass if the error occurs.
    with pytest.raises(Exception):
        handler(s3_event, None)

    # 4. Verify logging (inside the except block)
    # The 'capsys' fixture captures stdout/stderr.
    captured = capsys.readouterr()
    assert "[ERROR]" in captured.out or "Error:" in captured.out
