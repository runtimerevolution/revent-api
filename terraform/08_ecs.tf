# Cluster
resource "aws_ecs_cluster" "revent_development" {
  name = "${var.ecs_cluster_name}-cluster"
}

# Data templates
data "template_file" "revent_api_collectstatic" {
  template = file("templates/revent-api-collectstatic-task.json")
  vars = {
    docker_url_api = var.docker_url_api
    region         = var.region
  }
}
data "template_file" "revent_api_migrate" {
  template = file("templates/revent-api-migrate-task.json")
  vars = {
    docker_url_api = var.docker_url_api
    region         = var.region
    rds_db_name    = var.rds_db_name
    rds_db_schema  = var.rds_db_schema
    rds_username   = var.rds_username
    rds_password   = var.rds_password
    rds_port       = var.rds_port
    rds_hostname   = aws_db_instance.revent_development.address
  }
}
data "template_file" "revent_api_create_superuser" {
  template = file("templates/revent-api-create-superuser-task.json")
  vars = {
    docker_url_api              = var.docker_url_api
    region                      = var.region
    django_superuser_first_name = var.django_superuser_first_name
    django_superuser_last_name  = var.django_superuser_last_name
    django_superuser_email      = var.django_superuser_email
    django_superuser_password   = var.django_superuser_password
    rds_db_name                 = var.rds_db_name
    rds_db_schema               = var.rds_db_schema
    rds_username                = var.rds_username
    rds_password                = var.rds_password
    rds_port                    = var.rds_port
    rds_hostname                = aws_db_instance.revent_development.address
  }
}

data "template_file" "revent_nginx" {
  template = file("templates/revent-nginx-task.json")
  vars = {
    docker_url_api        = var.docker_url_api
    docker_url_app        = var.docker_url_app
    docker_url_nginx      = var.docker_url_nginx
    region                = var.region
    api_port              = 8000
    api_host              = "${aws_service_discovery_service.revent_nginx_sd.name}.${aws_service_discovery_private_dns_namespace.revent_ns.name}"
    app_port              = 3000
    app_host              = "${aws_service_discovery_service.revent_nginx_sd.name}.${aws_service_discovery_private_dns_namespace.revent_ns.name}"
    region                = var.region
    rds_db_name           = var.rds_db_name
    rds_db_schema         = var.rds_db_schema
    rds_username          = var.rds_username
    rds_password          = var.rds_password
    rds_port              = var.rds_port
    rds_hostname          = aws_db_instance.revent_development.address
    allowed_hosts         = aws_lb.revent_nginx_lb.dns_name
    allowed_redirect_uris = "${lower(aws_alb_listener.revent_nginx_alb_listener.protocol)}://${aws_lb.revent_nginx_lb.dns_name}"
    django_secret_key     = var.django_secret_key
    debug                 = var.debug
  }
}

# Task definitions
resource "aws_ecs_task_definition" "revent_api_migrate" {
  family                   = "revent-api-migrate-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.revent_ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.revent_ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_migrate.rendered
}

resource "aws_ecs_task_definition" "revent_api_create_superuser" {
  family                   = "revent-api-create-superuser-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.revent_ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.revent_ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_create_superuser.rendered
}

resource "aws_ecs_task_definition" "revent_api_collectstatic" {
  family                   = "revent-api-collectstatic-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.revent_ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.revent_ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_collectstatic.rendered
  volume {
    name = "efs-volume"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.revent_efs.id
      root_directory          = "/"
      transit_encryption      = "ENABLED"
      transit_encryption_port = 2049
      authorization_config {
        access_point_id = aws_efs_access_point.revent_app_access_point.id
        iam             = "ENABLED"
      }
    }
  }
}
resource "aws_ecs_task_definition" "revent_nginx" {
  family                   = "revent-nginx"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.revent_ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.revent_ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_nginx.rendered
  volume {
    name = "efs-volume"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.revent_efs.id
      root_directory          = "/"
      transit_encryption      = "ENABLED"
      transit_encryption_port = 2049
      authorization_config {
        access_point_id = aws_efs_access_point.revent_app_access_point.id
        iam             = "ENABLED"
      }
    }
  }
}

# Services

resource "aws_ecs_service" "revent_nginx" {
  name                              = "revent-nginx-service"
  cluster                           = aws_ecs_cluster.revent_development.id
  task_definition                   = aws_ecs_task_definition.revent_nginx.arn
  launch_type                       = "FARGATE"
  desired_count                     = 1
  health_check_grace_period_seconds = 30
  service_registries {
    registry_arn = aws_service_discovery_service.revent_nginx_sd.arn
  }
  network_configuration {
    subnets          = [aws_subnet.revent_public_subnet_1.id, aws_subnet.revent_public_subnet_2.id]
    security_groups  = [aws_security_group.revent_tasks_sg.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_alb_target_group.revent_nginx_tg.arn
    container_name   = "revent-nginx"
    container_port   = 80
  }
}

# File system
resource "aws_efs_file_system" "revent_efs" {
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }
}
resource "aws_efs_access_point" "revent_app_access_point" {
  file_system_id = aws_efs_file_system.revent_efs.id
  posix_user {
    uid = 1000
    gid = 1000
  }
  root_directory {
    path = "/efs"
    creation_info {
      owner_uid   = 1000
      owner_gid   = 1000
      permissions = "755"
    }
  }
}
resource "aws_efs_mount_target" "revent_efs_mount" {
  count           = length([aws_subnet.revent_public_subnet_1.id, aws_subnet.revent_public_subnet_2.id])
  file_system_id  = aws_efs_file_system.revent_efs.id
  subnet_id       = [aws_subnet.revent_public_subnet_1.id, aws_subnet.revent_public_subnet_2.id][count.index]
  security_groups = [aws_security_group.revent_efs_sg.id]
}
