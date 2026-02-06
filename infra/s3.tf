resource "aws_s3_bucket" "landing" {
  bucket = "${var.name_prefix}-landing"
}

resource "aws_s3_bucket_public_access_block" "landing_block" {
  bucket = aws_s3_bucket.landing.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "curated" {
  bucket = "${var.name_prefix}-curated"
}

resource "aws_s3_bucket_public_access_block" "curated_block" {
  bucket = aws_s3_bucket.curated.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
