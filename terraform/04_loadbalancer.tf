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

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_alb_listener" "revent_alb_listener" {
  load_balancer_arn = data.terraform_remote_state.shared.outputs.development_lb.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.revent_certificate.arn
  depends_on        = [aws_alb_target_group.revent_tg]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.revent_tg.arn
  }
}
