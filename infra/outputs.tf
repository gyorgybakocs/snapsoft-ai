output "lambda_name" {
  value = aws_lambda_function.processor.function_name
}

output "landing_bucket_name" {
  value = aws_s3_bucket.landing.bucket
}

output "curated_bucket_name" {
  value = aws_s3_bucket.curated.bucket
}
