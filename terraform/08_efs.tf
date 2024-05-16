# File system
resource "aws_efs_file_system" "revent_efs" {
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }
}
resource "aws_efs_access_point" "revent_app_access_point" {
  file_system_id = aws_efs_file_system.revent_efs.id
  posix_user {
    uid = 1000
    gid = 1000
  }
  root_directory {
    path = "/efs"
    creation_info {
      owner_uid   = 1000
      owner_gid   = 1000
      permissions = "755"
    }
  }
}
resource "aws_efs_mount_target" "revent_efs_mount" {
  count           = length(aws_default_subnet.default_subnets)
  file_system_id  = aws_efs_file_system.revent_efs.id
  subnet_id       = aws_default_subnet.default_subnets[count.index].id
  security_groups = [aws_security_group.efs_sg.id]
}
