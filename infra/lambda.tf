# Bundles the Python source code; used to detect changes and trigger function updates.
data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir = "${path.module}/../lambda"
  output_path = "${path.module}/.build/lambda.zip"
}

# The core compute resource that executes the data transformation logic.
resource "aws_lambda_function" "processor" {
  function_name = "${var.name_prefix}-processor"
  role = aws_iam_role.lambda_exec.arn

  # Runtime aligned with the provided Pandas layer version for compatibility.
  runtime = "python3.12"
  handler = "handler.handler"

  # Source code integrity check to ensure only the latest zipped code is deployed.
  filename = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  # Conservative limits; memory and time scaled for small-to-medium CSV processing.
  timeout = 30
  memory_size = 512

  # Dynamic configuration via environment variables for portability between stages.
  environment {
    variables = {
      TARGET_BUCKET = aws_s3_bucket.curated.id
      TARGET_PREFIX = "curated/"
    }
  }

  # Leverages an AWS-managed layer for Pandas to keep the deployment package lightweight.
  layers = ["arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python312:13"]
}
