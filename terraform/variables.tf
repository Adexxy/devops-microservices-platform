# This file defines the variables used in the Terraform configuration for the DevOps Microservices Platform.

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "project_name" {
  default = "devops-platform"
}

variable "cluster_name" {
  default = "devops-cluster"
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
}

variable "db_username" {
  description = "The username for the RDS database"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "azs" {
  description = "A list of availability zones in the region"
  type        = list(string)
}

variable "public_subnets" {
  description = "List of public subnet CIDRs"
  type        = list(string)
}

variable "private_subnets" {
  description = "List of private subnet CIDRs"
  type        = list(string)
}

variable "environment" {
  description = "The environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "eks_cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "s3_key" {
  description = "The key for the S3 object"
  type        = string
}

variable "db_name" {
    description = "The name of the RDS database"
    type        = string
    default     = "microservices_platform_db"
}

variable "db_user" {  
    description = "The username for the RDS database"
    type        = string
}

variable "db_password" {
    description = "The password for the RDS database"
    type        = string
}

variable "public_subnets_cidr" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
}
variable "private_subnets_cidr" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
}

# variable "node_role_arn" {
#   description = "The ARN of the IAM role for the EKS nodes"
#   type        = string
# }

variable "ecr_service_names" {
  description = "List of service names for ECR repositories"
  type        = list(string)
}