# Allow the landing bucket to invoke the Lambda function
resource "aws_lambda_permission" "allow_landing_invoke" {
  statement_id = "AllowLandingBucketInvoke"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processor.function_name
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.landing.arn
}

# Configure S3 event notification: when a .csv is uploaded -> invoke Lambda
resource "aws_s3_bucket_notification" "landing_object_created" {
  bucket = aws_s3_bucket.landing.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.processor.arn
    events = ["s3:ObjectCreated:*"]
    filter_prefix = "input/"
    filter_suffix = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_landing_invoke]
}
