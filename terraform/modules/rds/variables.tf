variable "subnet_ids" {
  description = "List of subnet IDs for the RDS subnet group"
  type        = list(string)
}

variable "db_user" {
  description = "Username for the RDS instance"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS instance"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name for the RDS instance"
  type        = string
}

variable "security_groups" {
  description = "List of security group IDs to associate with the RDS instance"
  type        = list(string)
}

variable "environment" {
  description = "Environment for the RDS instance (e.g., dev, prod)"
  type        = string
}
