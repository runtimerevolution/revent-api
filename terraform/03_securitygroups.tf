# ALB Security Group (Traffic Internet -> ALB)
resource "aws_security_group" "revent_load_balancer_sg" {
  name        = "load_balancer_security_group"
  description = "Security group for external load balancer serving Nginx"
  vpc_id      = aws_vpc.revent_development_vpc.id

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
resource "aws_security_group" "revent_tasks_sg" {
  name        = "ecs_fargate_security_group"
  description = "Allows inbound access from the ALB and allows communication among tasks within the security group"
  vpc_id      = aws_vpc.revent_development_vpc.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    self            = true
    security_groups = [aws_security_group.revent_load_balancer_sg.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS Security Group (traffic Fargate -> RDS)
resource "aws_security_group" "revent_rds_sg" {
  name        = "rds-security-group"
  description = "Allows inbound access from Fargate only"
  vpc_id      = aws_vpc.revent_development_vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    security_groups = [aws_security_group.revent_tasks_sg.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "revent_efs_sg" {
  name        = "EFS Security Group"
  description = "Allow ECS to EFS communication"
  vpc_id      = aws_vpc.revent_development_vpc.id

  ingress {
    from_port   = 2049  # NFS port
    to_port     = 2049
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Modify this based on your security requirements
  }
}