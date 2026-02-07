terraform {
  # Specifies mandatory providers to ensure reproducible infrastructure deployments.
  required_providers {
    # Version pinned to avoid breaking changes in the AWS resource model.
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    # Required for packaging the Lambda function code during the build phase.
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

# Regional configuration; influences data residency and layer ARN validity.
provider "aws" {
  region = var.aws_region
}

# Fetches metadata about the active AWS account to enable dynamic resource naming.
data "aws_caller_identity" "current" {}

locals {
  # Extracts the unique AWS Account ID to prevent cross-account S3 naming collisions.
  account_id = data.aws_caller_identity.current.account_id
  
  # Sanitizes the IAM user identity string to create a safe suffix for S3 bucket names.
  # This ensures global uniqueness even if multiple users deploy in the same account.
  user_suffix = replace(lower(data.aws_caller_identity.current.user_id), "/[^a-z0-9]/", "-")
}
