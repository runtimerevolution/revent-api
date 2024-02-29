resource "aws_service_discovery_private_dns_namespace" "revent_ns" {
  name        = "revent.local"
  description = "Service Discovery Private DNS Namespace for API"
  vpc         = aws_vpc.revent_development_vpc.id
}

resource "aws_service_discovery_service" "revent_nginx_sd" {
  name        = "revent-nginx-service-discovery"
  description = "Service Discovery Service for NGINX"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.revent_ns.id

    dns_records {
      ttl  = 300
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}
