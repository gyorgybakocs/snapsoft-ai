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
