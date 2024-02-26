resource "aws_db_subnet_group" "revent_development" {
  name       = "main"
  subnet_ids = [aws_subnet.revent_private_subnet_1.id, aws_subnet.revent_private_subnet_2.id]
}

resource "aws_db_instance" "revent_development" {
  identifier              = "development"
  db_name                 = var.rds_db_name
  username                = var.rds_username
  password                = var.rds_password
  port                    = var.rds_port
  engine                  = "postgres"
  engine_version          = "15.4"
  instance_class          = var.rds_instance_class
  allocated_storage       = "20"
  storage_encrypted       = false
  vpc_security_group_ids  = [aws_security_group.revent_rds_sg.id]
  db_subnet_group_name    = aws_db_subnet_group.revent_development.name
  multi_az                = false
  storage_type            = "gp2"
  publicly_accessible     = false
  backup_retention_period = 7
  skip_final_snapshot     = true
}