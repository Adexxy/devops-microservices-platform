# variables.tf
variable "service_names" {
  description = "List of microservices to create ECR repositories for"
  type        = list(string)
}

variable "environment" {
  description = "Environment for the ECR repositories (e.g., dev, prod)"
  type        = string
}
