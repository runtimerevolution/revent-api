resource "aws_db_subnet_group" "development" {
  name       = "development"
  subnet_ids = aws_default_subnet.default_subnets[*].id
}

resource "aws_db_instance" "development" {
  identifier              = "development"
  username                = var.rds_username
  password                = var.rds_password
  port                    = var.rds_port
  engine                  = "postgres"
  engine_version          = "15.4"
  instance_class          = var.rds_instance_class
  allocated_storage       = "20"
  storage_encrypted       = false
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.development.name
  multi_az                = false
  storage_type            = "gp2"
  publicly_accessible     = true
  backup_retention_period = 7
  skip_final_snapshot     = true
}
