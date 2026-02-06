resource "aws_s3_bucket" "landing" {
  bucket = "${var.name_prefix}-landing"
}

resource "aws_s3_bucket" "curated" {
  bucket = "${var.name_prefix}-curated"
}
