# Target group for ECS Fargate
resource "aws_alb_target_group" "revent_tg" {
  name        = "revent-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = data.terraform_remote_state.shared.outputs.vpc.id
  target_type = "ip"

  health_check {
    path     = var.health_check_path
    port     = "traffic-port"
    interval = 60
    matcher  = "200"
  }
}

resource "aws_lb_listener_rule" "revent_rule" {
  listener_arn = data.terraform_remote_state.shared.outputs.development_lb_listener.arn

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.revent_tg.arn
  }

  condition {
    host_header {
      values = [var.domain_name]
    }
  }
}
