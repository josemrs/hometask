aws_region  = "eu-west-2"
application = "hello-api"
environment = "develop"

vpc_name           = "develop-us-east-1"
vpc_description    = "Main develop VPC"
vpc_cidr           = "10.65.0.0/16"
availability_zones = ["eu-west-2a", "eu-west-2b", "eu-west-2c"]
private_subnets    = ["10.65.0.0/20", "10.65.16.0/20", "10.65.32.0/20"]
public_subnets     = ["10.65.208.0/20", "10.65.224.0/20", "10.65.240.0/20"]

public_subnet_tags = {
  "SubnetType"             = "Public"
  "kubernetes.io/role/elb" = "1"
}

private_subnet_tags = {
  "SubnetType"                      = "Private"
  "kubernetes.io/role/internal-elb" = "1"
}