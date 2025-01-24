resource "aws_cloudwatch_log_group" "revent_api_log_group" {
  name              = "/ecs/revent-api"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "revent_app_log_group" {
  name              = "/ecs/revent-app"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_group" "revent_nginx_log_group" {
  name              = "/ecs/revent-nginx"
  retention_in_days = var.log_retention_in_days
}

resource "aws_cloudwatch_log_stream" "revent_nginx_log_stream" {
  name           = "revent-nginx-log-stream"
  log_group_name = aws_cloudwatch_log_group.revent_nginx_log_group.name
}
