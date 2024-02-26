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

# networking

variable "revent_public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "revent_public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "revent_private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "revent_private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]
}
resource "null_resource" "revent_aws_availability_zones" {
  for_each = toset(var.availability_zones)
  triggers = {
    name = each.key
  }
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

# ECS service auto scaling

variable "autoscale_min" {
  description = "Minimum autoscale (number of tasks)"
  default     = "0"
}

variable "autoscale_max" {
  description = "Maximum autoscale (number of tasks)"
  default     = "1"
}

variable "autoscale_desired" {
  description = "Desired number of tasks to run initially"
  default     = "1"
}

# ecs

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "development"
}
variable "django_secret_key" {
  description = "Secret key for django configuration"
  default     = ""
}
variable "debug" {
  description = "Django debug configuration"
  default     = "False"
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