output "revent_nginx_lb_hostname" {
  value = aws_lb.revent_lb.dns_name
}

output "subnets" {
  value = aws_default_subnet.default_subnets[*].id
}

output "security_group" {
  value = aws_security_group.tasks_sg.id
}

