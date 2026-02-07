# Grants S3 the specific permission to invoke the processor function.
resource "aws_lambda_permission" "allow_landing_invoke" {
  statement_id  = "AllowLandingBucketInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.landing.arn
}

# Event notification setup: triggers the pipeline only for .csv files in the 'input/' prefix.
resource "aws_s3_bucket_notification" "landing_object_created" {
  bucket = aws_s3_bucket.landing.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "input/"
    filter_suffix       = ".csv"
  }

  # Ensure permissions exist before S3 attempts to configure the notification.
  depends_on = [aws_lambda_permission.allow_landing_invoke]
}
