# Useful for operational tasks like checking logs or manual function invocation.
output "lambda_name" {
  value = aws_lambda_function.processor.function_name
}

# Identifies the source bucket for manual or automated data ingestion tests.
output "landing_bucket_name" {
  value = aws_s3_bucket.landing.bucket
}

# Identifies the output location for verifying successful data transformations.
output "curated_bucket_name" {
  value = aws_s3_bucket.curated.bucket
}
