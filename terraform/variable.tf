variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
variable "key-name" {
  type        = string
  default     = "redis-infra-key"
  description = "AWS Key Pair name for EC2 instances"
}
