# Defines the identity under which the Lambda function operates.
resource "aws_iam_role" "lambda_exec" {
  name = "${var.name_prefix}-lambda-exec"

  # Standard trust policy allowing the Lambda service to assume this role.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# Essential for observability; grants permission to write execution logs to CloudWatch.
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Defines granular data access: restricted to landing (read) and curated (write) buckets.
resource "aws_iam_policy" "lambda_s3_access" {
  name        = "${var.name_prefix}-lambda-s3-access"
  description = "Allow Lambda to read from landing bucket and write to curated bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "ReadLanding"
        Effect = "Allow"
        Action = ["s3:GetObject"]
        Resource = ["${aws_s3_bucket.landing.arn}/*"]
      },
      {
        Sid = "WriteCurated"
        Effect = "Allow"
        Action = ["s3:PutObject"]
        Resource = ["${aws_s3_bucket.curated.arn}/*"]
      }
    ]
  })
}

# Finalizes the security setup by binding the S3 policy to the Lambda role.
resource "aws_iam_role_policy_attachment" "lambda_s3_access" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}
