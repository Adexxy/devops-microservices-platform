# EKS Outputs
output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "rds_endpoint" {
  value = module.rds.endpoint
}


# VPC Outputs
output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "VPC ID"
}

output "public_subnet_ids" {
  value       = module.vpc.public_subnet_ids
  description = "List of public subnet IDs"
}

output "private_subnet_ids" {
  value       = module.vpc.private_subnet_ids
  description = "List of private subnet IDs"
}

output "private_sg_id" {
  value       = module.vpc.private_sg_id
  description = "Private security group ID"
}

# # RDS Outputs
# output "rds_endpoint" {
#   value       = module.rds.db_endpoint
#   description = "RDS endpoint"
# }

# output "rds_db_name" {
#   value       = module.rds.db_name
#   description = "RDS database name"
# }

# output "rds_db_port" {
#   value       = module.rds.db_port
#   description = "RDS port"
# }

# ECR Outputs
# output "ecr_repository_url" {
#   value       = module.ecr.repository_url
#   description = "ECR repository URL"
# }

# output "ecr_repository_name" {
#   value       = module.ecr.repository_name
#   description = "ECR repository name"
# }