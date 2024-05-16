variable "region" {
  description = "The AWS region to create resources in."
}

variable "docker_url_nginx" {
  description = "Docker image to run NGINX in the ECS cluster"
}
variable "docker_url_api" {
  description = "Docker image to run the API in the ECS cluster"
}
variable "docker_url_app" {
  description = "Docker image to run the APP in the ECS cluster"
}

variable "fargate_cpu" {
  description = "Amount of CPU for Fargate task. E.g., '256' (.25 vCPU)"
  default     = "256"
}
variable "fargate_memory" {
  description = "Amount of memory for Fargate task. E.g., '512' (0.5GB)"
  default     = "512"
}
variable "fargate_os" {
  description = "Fargate tasks operating system"
  default     = "LINUX"
}
variable "fargate_cpu_arch" {
  description = "Fargate tasks CPU architecture"
  default     = "ARM64"
}

# load balancer
variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/ping/"
}

# logs
variable "log_retention_in_days" {
  default = 7
}

# ecs
variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "revent"
}

variable "rds_db_name" {
  description = "RDS database name"
}
variable "rds_db_schema" {
  description = "RDS database schema"
}
variable "rds_username" {
  description = "RDS database username"
}
variable "rds_password" {
  description = "RDS database password"
}
variable "rds_port" {
  description = "RDS database port"
}
variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t3.micro"
}

# s3
variable "s3_storage_bucket" {
  description = "S3 storage bucket name"
  default     = "revent-storage"
}
variable "s3_env_bucket" {
  description = "S3 env bucket name"
  default     = "revent-env"
}
