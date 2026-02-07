locals {
  # Extracts the unique AWS Account ID to prevent cross-account S3 naming collisions.
  account_id = data.aws_caller_identity.current.account_id

  # Sanitizes the IAM user identity string to create a safe suffix for S3 bucket names.
  # This ensures global uniqueness even if multiple users deploy in the same account.
  user_suffix = replace(lower(data.aws_caller_identity.current.user_id), "/[^a-z0-9]/", "-")
}
