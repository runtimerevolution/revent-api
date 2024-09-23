# Makefile used to manage Terraform commands
.DEFAULT_GOAL := help

include .env
export

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


init: # Initialize Terraform's working directory
	terraform init

plan: # View the changes that are required by the current infrastructure's configuration 
	terraform plan

json: # Export the plan into a JSON file that can be read by Rover
	terraform plan -out plan.out
	terraform show -json plan.out > plan.json
	rm plan.out

apply: # Create or update the infrastructure
	terraform apply

destroy: # Destroy previously-created infrastructure
	terraform destroy

build: # Build docker images and push them to ECR
	aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_URL}
	docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_api} . && docker push ${TF_VAR_docker_url_api}
	cd ${APP_PATH} && docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_app} . && docker push ${TF_VAR_docker_url_app}
	cd nginx && docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_nginx} . && docker push ${TF_VAR_docker_url_nginx}