# variables.tf
variable "service_names" {
  description = "List of microservices to create ECR repositories for"
  type        = list(string)
}

