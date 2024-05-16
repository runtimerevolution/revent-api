resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "ecs-task-execution-role"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role_policy" "ecs_task_execution_role_policy" {
  name   = "ecs-task-execution-role-policy"
  policy = file("policies/ecs-task-execution-policy.json")
  role   = aws_iam_role.ecs_task_execution_role.id
}

resource "aws_iam_role" "ecs_service_role" {
  name               = "ecs-service-role"
  assume_role_policy = file("policies/ecs-role.json")
}

resource "aws_iam_role_policy" "ecs_service_role_policy" {
  name   = "ecs-service-role-policy"
  policy = file("policies/ecs-service-role-policy.json")
  role   = aws_iam_role.ecs_service_role.id
}
