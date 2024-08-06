resource "aws_security_group" "pod-isolation" {
  name        = "${var.environment}-public-sg"
  description = "EKS Public Security Group"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description = "Allow self ingress"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    self        = true
  }

  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common-tags,
    tomap({
      "Instance" = "${var.environment}-public-sg"
      "Role"     = "security-group"
    })
  )
}