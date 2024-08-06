variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "environment" {
  type = string
}

variable "application" {
  type    = string
  default = "hello-api"
}

# VPC Variables
variable "vpc_name" {
  type = string
}

variable "vpc_description" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "availability_zones" {
  type = list(any)
}

variable "private_subnets" {
  description = "Private subnet CIDRs"
  type        = list(any)
}

variable "public_subnets" {
  description = "Private subnet CIDRs"
  type        = list(any)
}

variable "public_subnet_tags" {
  description = "Additional tags for the public subnets"
  type        = map(string)
  default     = {}
}

variable "private_subnet_tags" {
  description = "Additional tags for the public subnets"
  type        = map(string)
  default     = {}
}