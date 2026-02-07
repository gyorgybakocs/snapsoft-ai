# Fetches metadata about the active AWS account to enable dynamic resource naming.
data "aws_caller_identity" "current" {}
