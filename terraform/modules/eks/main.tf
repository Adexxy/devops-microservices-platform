resource "aws_eks_cluster" "microservices_cluster" {
  name = var.cluster_name

  access_config {
    authentication_mode = "API"
  }

  role_arn = aws_iam_role.cluster.arn
  version  = "1.32"

  vpc_config {
    subnet_ids = var.private_subnets
  }

  # Ensure that IAM Role permissions are created before and deleted
  # after EKS Cluster handling. Otherwise, EKS will not be able to
  # properly delete EKS managed EC2 infrastructure such as Security Groups.

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
  ]

  tags = {
    Name        = "eks-cluster-${var.cluster_name}"
    Environment = var.environment
  }
}

resource "aws_iam_role" "cluster" {
  name = "eks-cluster-${var.cluster_name}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}



















# # Module: `modules/eks/main.tf`
# module "eks" {
#   source          = "terraform-aws-modules/eks/aws"
#   cluster_name    = var.cluster_name
#   cluster_version = "1.27"

#   subnet_ids      = var.subnet_ids
#   vpc_id          = var.vpc_id

#   eks_managed_node_groups = {
#     default = {
#       desired_capacity = 2
#       max_capacity     = 3
#       min_capacity     = 1

#       instance_types = ["t3.medium"]
#       iam_role_arn   = var.node_role_arn
#     }
#   }

# }

