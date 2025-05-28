terraform {
  backend "s3" {
    bucket = "microservices-platform-terraform-state"
    key    = "terraform/terraform.tfstate"
    encrypt = true
    dynamodb_table = "microservices-platform-terraform-locks"
    region = "us-east-1"
  }
}
