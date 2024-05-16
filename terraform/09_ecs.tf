# Cluster
resource "aws_ecs_cluster" "revent_development" {
  name = "${var.ecs_cluster_name}-cluster"
}

# Data templates
data "template_file" "revent_api" {
  template = file("templates/revent-api-task.json")
  vars = {
    region                = var.region
    docker_url_api        = var.docker_url_api
    docker_url_app        = var.docker_url_app
    docker_url_nginx      = var.docker_url_nginx
    api_env_file          = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_api_env.key}"
    app_env_file          = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_app_env.key}"
    nginx_env_file        = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_nginx_env.key}"
    rds_hostname          = aws_db_instance.development.address
    allowed_hosts         = aws_lb.revent_lb.dns_name
    allowed_redirect_uris = "${lower(aws_alb_listener.revent_alb_listener.protocol)}://${aws_lb.revent_lb.dns_name}"
    s3_endpoint_url       = "http://${aws_s3_bucket.revent_storage_bucket.bucket_regional_domain_name}"
    revent_media_dir      = "revent-media/"
  }
}
data "template_file" "revent_api_collectstatic" {
  template = file("templates/revent-api-collectstatic-task.json")
  vars = {
    region         = var.region
    docker_url_api = var.docker_url_api
    api_env_file   = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_api_env.key}"
  }
}
data "template_file" "revent_api_migrate" {
  template = file("templates/revent-api-migrate-task.json")
  vars = {
    region         = var.region
    docker_url_api = var.docker_url_api
    api_env_file   = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_api_env.key}"
    rds_hostname   = aws_db_instance.development.address
  }
}
data "template_file" "revent_api_create_superuser" {
  template = file("templates/revent-api-create-superuser-task.json")
  vars = {
    region         = var.region
    docker_url_api = var.docker_url_api
    api_env_file   = "${aws_s3_bucket.revent_env_bucket.arn}/${aws_s3_object.revent_api_env.key}"
    rds_hostname   = aws_db_instance.development.address
  }
}

# Task definitions
resource "aws_ecs_task_definition" "revent_api" {
  family                   = "revent-api"
  depends_on               = [aws_db_instance.development]
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api.rendered
  runtime_platform {
    operating_system_family = var.fargate_os
    cpu_architecture        = var.fargate_cpu_arch
  }
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
resource "aws_ecs_task_definition" "revent_api_migrate" {
  family                   = "revent-api-migrate-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_migrate.rendered
  runtime_platform {
    operating_system_family = var.fargate_os
    cpu_architecture        = var.fargate_cpu_arch
  }
}

resource "aws_ecs_task_definition" "revent_api_create_superuser" {
  family                   = "revent-api-create-superuser-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_create_superuser.rendered
  runtime_platform {
    operating_system_family = var.fargate_os
    cpu_architecture        = var.fargate_cpu_arch
  }
}

resource "aws_ecs_task_definition" "revent_api_collectstatic" {
  family                   = "revent-api-collectstatic-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions    = data.template_file.revent_api_collectstatic.rendered
  runtime_platform {
    operating_system_family = var.fargate_os
    cpu_architecture        = var.fargate_cpu_arch
  }
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
resource "aws_ecs_service" "revent" {
  name                   = "revent-service"
  cluster                = aws_ecs_cluster.revent_development.id
  task_definition        = aws_ecs_task_definition.revent_api.arn
  launch_type            = "FARGATE"
  desired_count          = 1
  enable_execute_command = true
  network_configuration {
    subnets          = aws_default_subnet.default_subnets[*].id
    security_groups  = [aws_security_group.tasks_sg.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_alb_target_group.revent_tg.arn
    container_name   = "revent-nginx"
    container_port   = 80
  }
}
