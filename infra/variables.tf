# Region pinned to Frankfurt for proximity and layer availability (Pandas layer).
variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "eu-central-1"
}

# Global prefix to avoid naming collisions in the global S3 namespace.
variable "name_prefix" {
  type        = string
  description = "Global-unique prefix for resource names (better than a random...)"
  default     = "snapsoft"
}
