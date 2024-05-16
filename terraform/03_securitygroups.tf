# ALB Security Group (Traffic Internet -> ALB)
resource "aws_security_group" "lb_sg" {
  name        = "load_balancer_security_group"
  description = "Security group for external load balancer serving Nginx"
  vpc_id      = aws_default_vpc.default_vpc.id

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

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Fargate Security group (traffic ALB -> ECS Fargate Tasks)
resource "aws_security_group" "tasks_sg" {
  name        = "tasks_security_group"
  description = "Allows inbound access from the ALB and allows communication among tasks within the security group"
  vpc_id      = aws_default_vpc.default_vpc.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.lb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS Security Group (traffic Fargate -> RDS)
resource "aws_security_group" "rds_sg" {
  name        = "rds-security-group"
  description = "Allows inbound access from Fargate only"
  vpc_id      = aws_default_vpc.default_vpc.id

  ingress {
    from_port       = var.rds_port
    to_port         = var.rds_port
    protocol        = "tcp"
    security_groups = [aws_security_group.tasks_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EFS Security Group (traffic Fargate -> EFS)
resource "aws_security_group" "efs_sg" {
  name        = "EFS Security Group"
  description = "Allow ECS to EFS communication"
  vpc_id      = aws_default_vpc.default_vpc.id

  ingress {
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [aws_security_group.tasks_sg.id]
  }
}
