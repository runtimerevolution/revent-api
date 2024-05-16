# Load Balancer
resource "aws_lb" "revent_lb" {
  name               = "revent"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_default_subnet.default_subnets[*].id
}

# Target group for ECS Fargate
resource "aws_alb_target_group" "revent_tg" {
  name        = "revent-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_default_vpc.default_vpc.id
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
  load_balancer_arn = aws_lb.revent_lb.id
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.revent_tg]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.revent_tg.arn
  }
}
