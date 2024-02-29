# Targets
resource "aws_appautoscaling_target" "revent_nginx_target" {
  max_capacity       = var.autoscale_max
  min_capacity       = var.autoscale_min
  resource_id        = "service/${aws_ecs_cluster.revent_development.name}/${aws_ecs_service.revent_nginx.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  depends_on         = [aws_ecs_service.revent_nginx]
}

# Policies
resource "aws_appautoscaling_policy" "revent_nginx_policy" {
  name               = "revent-nginx-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.revent_nginx_target.resource_id
  scalable_dimension = aws_appautoscaling_target.revent_nginx_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.revent_nginx_target.service_namespace
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 75
    scale_in_cooldown  = 300
    scale_out_cooldown = 300
  }
}
