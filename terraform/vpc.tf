resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = merge(
    local.common-tags,
    tomap({
      "Instance"    = var.vpc_name,
      "Name"        = var.vpc_name,
      "Description" = var.vpc_description
      "Role"        = "vpc"
    })
  )
}