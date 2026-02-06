data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir = "${path.module}/../lambda"
  output_path = "${path.module}/.build/lambda.zip"
}

resource "aws_lambda_function" "processor" {
  function_name = "${var.name_prefix}-processor"
  role = aws_iam_role.lambda_exec.arn

  runtime = "python3.12"
  handler = "handler.handler"

  filename = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout = 10
  memory_size = 512

  # Injecting bucket names and prefixes from Terraform locals/variables
  environment {
    variables = {
      TARGET_BUCKET = aws_s3_bucket.curated.id
      TARGET_PREFIX = "curated/"
    }
  }

  # Managed AWS Layer for Pandas (optimized for Python 3.12)
  layers = ["arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python312:13"]
}
