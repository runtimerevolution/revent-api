# Development VPC
resource "aws_vpc" "revent_development_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

# Public subnets
resource "aws_subnet" "revent_public_subnet_1" {
  cidr_block        = var.revent_public_subnet_1_cidr
  vpc_id            = aws_vpc.revent_development_vpc.id
  availability_zone = var.availability_zones[0]
}
resource "aws_subnet" "revent_public_subnet_2" {
  cidr_block        = var.revent_public_subnet_2_cidr
  vpc_id            = aws_vpc.revent_development_vpc.id
  availability_zone = var.availability_zones[1]
}

# Private subnets
resource "aws_subnet" "revent_private_subnet_1" {
  cidr_block        = var.revent_private_subnet_1_cidr
  vpc_id            = aws_vpc.revent_development_vpc.id
  availability_zone = var.availability_zones[0]
}
resource "aws_subnet" "revent_private_subnet_2" {
  cidr_block        = var.revent_private_subnet_2_cidr
  vpc_id            = aws_vpc.revent_development_vpc.id
  availability_zone = var.availability_zones[1]
}

# Route tables for the subnets
resource "aws_route_table" "revent_public_route_table" {
  vpc_id = aws_vpc.revent_development_vpc.id
}
resource "aws_route_table" "revent_private_route_table" {
  vpc_id = aws_vpc.revent_development_vpc.id
}

# Associate the newly created route tables to the subnets
resource "aws_route_table_association" "revent_public_route_1_association" {
  route_table_id = aws_route_table.revent_public_route_table.id
  subnet_id      = aws_subnet.revent_public_subnet_1.id
}
resource "aws_route_table_association" "revent_public_route_2_association" {
  route_table_id = aws_route_table.revent_public_route_table.id
  subnet_id      = aws_subnet.revent_public_subnet_2.id
}
resource "aws_route_table_association" "revent_private_route_1_association" {
  route_table_id = aws_route_table.revent_private_route_table.id
  subnet_id      = aws_subnet.revent_private_subnet_1.id
}
resource "aws_route_table_association" "revent_private_route_2_association" {
  route_table_id = aws_route_table.revent_private_route_table.id
  subnet_id      = aws_subnet.revent_private_subnet_2.id
}

# Elastic IP
resource "aws_eip" "revent_eip_nat_gw" {
  domain                    = "vpc"
  associate_with_private_ip = "10.0.0.5"
  depends_on                = [aws_internet_gateway.revent_development_igw]
}

# NAT gateway
resource "aws_nat_gateway" "revent_nat_gw" {
  allocation_id = aws_eip.revent_eip_nat_gw.id
  subnet_id     = aws_subnet.revent_public_subnet_1.id
  depends_on    = [aws_eip.revent_eip_nat_gw]
}
resource "aws_route" "revent_route_nat_gw" {
  route_table_id         = aws_route_table.revent_private_route_table.id
  nat_gateway_id         = aws_nat_gateway.revent_nat_gw.id
  destination_cidr_block = "0.0.0.0/0"
}

# Internet Gateway for the public subnet
resource "aws_internet_gateway" "revent_development_igw" {
  vpc_id = aws_vpc.revent_development_vpc.id
}

# Route the public subnet traffic through the Internet Gateway
resource "aws_route" "revent_public_internet_igw_route" {
  route_table_id         = aws_route_table.revent_public_route_table.id
  gateway_id             = aws_internet_gateway.revent_development_igw.id
  destination_cidr_block = "0.0.0.0/0"
}