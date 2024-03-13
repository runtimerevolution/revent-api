# Load Balancer
resource "aws_lb" "revent_api_lb" {
  name               = "revent-api-lb"
  load_balancer_type = "application"
  internal           = true
  security_groups    = [aws_security_group.revent_load_balancer_sg.id]
  subnets            = [aws_subnet.revent_private_subnet_1.id, aws_subnet.revent_private_subnet_2.id]
}

resource "aws_lb" "revent_nginx_lb" {
  name               = "revent-nginx-lb"
  load_balancer_type = "application"
  internal           = false
  security_groups    = [aws_security_group.revent_load_balancer_sg.id]
  subnets            = [aws_subnet.revent_public_subnet_1.id, aws_subnet.revent_public_subnet_2.id]
}

# Target group for ECS Fargate
resource "aws_alb_target_group" "revent_api_tg" {
  name        = "revent-api-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.revent_development_vpc.id
  target_type = "ip"

  health_check {
    path     = var.health_check_path
    port     = "traffic-port"
    interval = 60
    matcher  = "200"
  }
}

resource "aws_alb_target_group" "revent_nginx_tg" {
  name        = "revent-nginx-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.revent_development_vpc.id
  target_type = "ip"

  health_check {
    path     = var.health_check_path
    port     = "traffic-port"
    interval = 60
    matcher  = "200"
  }
}

# Listener (redirects traffic from the load balancer to the target group)
resource "aws_alb_listener" "revent_api_alb_listener" {
  load_balancer_arn = aws_lb.revent_api_lb.id
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.revent_api_tg]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.revent_api_tg.arn
  }
}

resource "aws_alb_listener" "revent_nginx_alb_listener" {
  load_balancer_arn = aws_lb.revent_nginx_lb.id
  port              = "80"
  protocol          = "HTTP"
  depends_on        = [aws_alb_target_group.revent_nginx_tg]

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.revent_nginx_tg.arn
  }
}
