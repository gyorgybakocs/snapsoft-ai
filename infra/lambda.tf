data "archive_file" "lambda_zip" {
  type = "zip"
  source_file = "${path.module}/../lambda/handler.py"
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
  memory_size = 128
}
