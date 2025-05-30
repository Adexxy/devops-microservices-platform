# Module: `modules/rds/main.tf`
resource "aws_db_subnet_group" "postres_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "17.2"
  instance_class       = "db.t3.micro"
  username             = var.db_user
  password             = var.db_password
  skip_final_snapshot  = true
  publicly_accessible  = false
  vpc_security_group_ids = var.security_groups
  db_name              = var.db_name
  db_subnet_group_name = aws_db_subnet_group.postres_subnet_group.name
  
  tags = {
    Name = "postgres-db-instance"
    Environment = var.environment
  }
}



