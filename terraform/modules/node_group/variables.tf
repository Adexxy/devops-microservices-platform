variable "cluster_name" {
  type        = string
  description = "Name of the EKS cluster"
}

variable "node_group_name" {
  type        = string
  description = "Name of the node group"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnets for the node group"
}

variable "node_role_arn" {
  type        = string
  description = "IAM role ARN for EKS worker nodes"
}

variable "instance_types" {
  type        = list(string)
  default     = ["t3.medium"]
  description = "EC2 instance types for worker nodes"
}

variable "desired_capacity" {
  type        = number
  default     = 2
  description = "Desired number of worker nodes"
}

variable "min_size" {
  type        = number
  default     = 1
  description = "Minimum number of worker nodes"
}

variable "max_size" {
  type        = number
  default     = 3
  description = "Maximum number of worker nodes"
}

variable "environment" {
  type        = string
  description = "Environment (e.g., dev, prod)"
}
