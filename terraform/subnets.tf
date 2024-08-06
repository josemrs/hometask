resource "aws_subnet" "private_subnet" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    local.common-tags,
    tomap({
      "Instance" = "${var.environment}-private-subnet-${var.availability_zones[count.index]}"
      "Name"     = "${var.environment}-private-subnet-${var.availability_zones[count.index]}"
      "Role"     = "private-subnet"
    })
  )
}

resource "aws_subnet" "public_subnet" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    local.common-tags,
    tomap({
      "Instance" = "${var.environment}-private-subnet-${var.availability_zones[count.index]}"
      "Name"     = "${var.environment}-private-subnet-${var.availability_zones[count.index]}"
      "Role"     = "private-subnet"
    })
  )
}
