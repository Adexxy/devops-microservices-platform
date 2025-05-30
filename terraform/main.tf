# Root main.tf to pull all modules together

module "vpc" {
  source                = "./modules/vpc"
  name                  = var.vpc_name
  vpc_name              = var.vpc_name
  aws_region            = var.aws_region
  azs                   = var.azs
  vpc_cidr              = var.vpc_cidr
  public_subnets        = var.public_subnets
  private_subnets       = var.private_subnets
  public_subnets_cidr   = var.public_subnets_cidr
  private_subnets_cidr  = var.private_subnets_cidr
  environment           = var.environment
}

module "iam" {
  source      = "./modules/iam"
  environment = var.environment
}

module "eks" {
  source         = "./modules/eks"
  subnet_ids     = module.vpc.private_subnet_ids
  vpc_id         = module.vpc.vpc_id
  cluster_name   = var.eks_cluster_name
  azs            = var.azs
  private_subnets = module.vpc.private_subnet_ids 
  environment    = var.environment 
}

module "rds" {
  source         = "./modules/rds"
  db_name        = var.db_name
  db_user        = var.db_username
  db_password    = var.db_password
  subnet_ids     = module.vpc.private_subnet_ids
  security_groups = [module.vpc.private_sg_id]
  environment    = var.environment
}

# module "s3" {
#   source      = "./modules/s3"
#   bucket-name = var.s3_bucket_name
# }

module "ecr" {
  source        = "./modules/ecr"
  service_names = var.ecr_service_names
  environment   = var.environment
}

module "node_group" {
  source            = "./modules/node_group"
  cluster_name      = var.eks_cluster_name
  node_group_name   = "${var.environment}-node-group"
  subnet_ids        = module.vpc.private_subnet_ids
  node_role_arn     = module.iam.eks_node_group_role_arn
  instance_types    = ["t3.medium"]      # or your preferred type
  desired_capacity  = 2
  min_size          = 1
  max_size          = 3
  environment       = var.environment

  depends_on = [module.eks]
}
