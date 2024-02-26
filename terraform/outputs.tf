output "revent_nginx_lb_hostname" {
  value = aws_lb.revent_nginx_lb.dns_name
}

output "subnets" {
  value = [aws_subnet.revent_public_subnet_1.id, aws_subnet.revent_public_subnet_2.id]
}

output "security_group" {
  value = aws_security_group.revent_tasks_sg.id
}

