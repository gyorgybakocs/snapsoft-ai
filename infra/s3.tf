# Entry point for raw CSV files; acts as the trigger source for the pipeline.
# Dynamically named with account ID and user suffix to ensure global uniqueness.
resource "aws_s3_bucket" "landing" {
  bucket = "${var.name_prefix}-landing-${local.account_id}-${local.user_suffix}"
  force_destroy = true 
}

# Public access is strictly blocked to protect potentially sensitive PII in raw data.
resource "aws_s3_bucket_public_access_block" "landing_block" {
  bucket = aws_s3_bucket.landing.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

# Storage for cleaned and normalized datasets ready for ML consumption.
# Uses dynamic naming to prevent "BucketAlreadyExists" errors during deployment.
resource "aws_s3_bucket" "curated" {
  bucket = "${var.name_prefix}-curated-${local.account_id}-${local.user_suffix}"
  force_destroy = true
}

# Standard security hardening to ensure data integrity in the curated zone.
resource "aws_s3_bucket_public_access_block" "curated_block" {
  bucket = aws_s3_bucket.curated.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
