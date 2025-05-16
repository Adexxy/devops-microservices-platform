provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  cidr_block = var.vpc_cidr
}

module "eks" {
  source          = "./modules/eks"
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  subnets         = module.vpc.public_subnets
}

module "rds" {
  source           = "./modules/rds"
  db_name          = var.db_name
  db_username      = var.db_username
  db_password      = var.db_password
  vpc_security_group_ids = [module.vpc.default_sg]
  subnet_ids       = module.vpc.private_subnets
}