resource "aws_vpc" "microservices-vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = var.vpc_name
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "microservices" {
  vpc_id = aws_vpc.microservices-vpc.id
  tags = {
    Name = "${var.vpc_name}-igw"
    Environment = var.environment
  }
}

resource "aws_subnet" "public_subnets" {
  count = length(var.public_subnets)
  vpc_id = aws_vpc.microservices-vpc.id
  cidr_block = var.public_subnets_cidr[count.index]
  availability_zone = element(var.azs, count.index)

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-${count.index + 1}"
    Environment = var.environment
  }
}

resource "aws_subnet" "private_subnets" {
  count = length(var.private_subnets)
  vpc_id = aws_vpc.microservices-vpc.id
  cidr_block = var.private_subnets_cidr[count.index]
  availability_zone = element(var.azs, count.index)

  tags = {
    Name = "${var.name}-private-${count.index + 1}"
    Environment = var.environment
  }
}

resource "aws_eip" "microservices_nat" {

  tags = {
    Name = "${var.name}-nat-eip"
    Environment = var.environment
  }
}

resource "aws_nat_gateway" "microservices_nat" {
  allocation_id = aws_eip.microservices_nat.id
  subnet_id = aws_subnet.public_subnets[0].id

  tags = {
    Name = "${var.name}-nat-gateway"
    Environment = var.environment
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.microservices-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.microservices.id
  }
  tags = {
    Name = "${var.name}-public-rt"
    Environment = var.environment
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.microservices-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.microservices_nat.id
  }

  tags = {
    Name = "${var.name}-private-rt"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public_subnets)
  subnet_id = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = length(aws_subnet.private_subnets)
  subnet_id = aws_subnet.private_subnets[count.index].id
  route_table_id = aws_route_table.private.id
}

# Security Group for the VPC
// Public SG: For resources in public subnets (e.g., ALB, bastion)
resource "aws_security_group" "public_sg" {
  name        = "${var.name}-public-sg"
  description = "Security group for public subnet resources"
  vpc_id      = aws_vpc.microservices-vpc.id

  // Example: Allow HTTP/HTTPS from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  // Egress: Allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${var.name}-public-sg"
    Environment = var.environment
  }
}

// Private SG: For resources in private subnets (e.g., EKS nodes, RDS)
resource "aws_security_group" "private_sg" {
  name        = "${var.name}-private-sg"
  description = "Security group for private subnet resources"
  vpc_id      = aws_vpc.microservices-vpc.id

  // Example: Allow all traffic from within the VPC
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_vpc.microservices-vpc.cidr_block]
  }
  // Egress: Allow all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${var.name}-private-sg"
    Environment = var.environment
  }
}

