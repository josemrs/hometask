# Required envvars

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY


# Usage

terraform plan -var-file variables.tfvars -out plan.out
terraform apply plan.out