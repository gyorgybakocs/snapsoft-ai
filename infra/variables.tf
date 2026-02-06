variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "eu-central-1"
}

variable "name_prefix" {
  type        = string
  description = "Global-unique prefix for resource names (better than a random...)"
  default     = "snapsoft-bgds-example"
}
