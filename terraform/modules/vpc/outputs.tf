output "vpc_id" {
  value = aws_vpc.microservices-vpc.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value = [for subnet in aws_subnet.public_subnets : subnet.id]
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value = [for subnet in aws_subnet.private_subnets : subnet.id]
}

output "public_sg_id" {
  value = aws_security_group.public_sg.id
}

output "private_sg_id" {
  value = aws_security_group.private_sg.id
}

output "vpc_security_group_ids" {
  description = "List of security group IDs for the VPC"
  value = [
    aws_security_group.public_sg.id,
    aws_security_group.private_sg.id
  ]
  
}

# output "default_sg_id" {
#   value = aws_security_group.microservices_sg.id
# }

# output "private_subnet_ids" {
#   value = aws_subnet.private_subnet_ids[*].id
# }

# output "private_subnets" {
#   description = "List of private subnet IDs"
#   value       = aws_subnet.private_subnets[*].id
# }
