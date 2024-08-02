.DEFAULT_GOAL := help

# include .env
export

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Pass arguments to the test command
ifeq (test,$(firstword $(MAKECMDGOALS)))
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(TEST_ARGS):;@:)
endif

up: # Start the docker containers
	$(eval include .env/docker/main.env)
	docker compose up -d

down: # Stop the docker containers
	$(eval include .env/docker/main.env)
	docker compose down -t 1

pre: # Run pre-commit
	$(eval include .env/local/api.env)
	pre-commit run --all-files


setup: up install migrate # Setup

coverage: # Get test coverage
	$(eval include .env/local/api.env)
	coverage erase && coverage run manage.py test && coverage html --skip-empty --skip-covered
	open htmlcov/index.html

test: # Test all django apps OR pass testing target like "smart_replenishment" or "planner_requests.tests.csv_file"
	$(eval include .env/local/api.env)
	poetry run python manage.py test --no-input $(TEST_ARGS)

populate: # Generate dummy data
	$(eval include .env/local/api.env)
	poetry run python launch.py

# Admin
superuser: createsuperuser # Create admin user
run: runserver # Run the django server
migrations: makemigrations # Create new django migrations
migrate: # Migrate all new django migrations
shell: # Launch python shell
urls: show_urls # Show server urls

local_commands = createsuperuser runserver makemigrations migrate shell show_urls

$(local_commands):
ifeq ($(or $(env),local),local)
	$(eval include .env/local/api.env)
	python manage.py $@
endif
ifeq ($(env),docker)
	$(eval include .env/docker/main.env)
	docker-compose exec revent-api python manage.py $@
endif

build: # Build docker images and store them in ECR
	$(eval include .env/terraform/main.env)
	aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_URL}
	docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_api} . && docker push ${TF_VAR_docker_url_api}
	cd ${APP_PATH} && docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_app} . && docker push ${TF_VAR_docker_url_app}
	cd nginx && docker buildx build --platform=linux/arm64 -t ${TF_VAR_docker_url_nginx} . && docker push ${TF_VAR_docker_url_nginx}

init: # Use terraform to initialize the project
plan: # Use terraform to view changes made to the infrastructure
apply: # Use terraform to create or modify the infrastructure
destroy: # Use terraform to destroy the infrastructure

terraform_commands = init plan apply destroy

$(terraform_commands):
	$(eval include .env/terraform/main.env)
	$(eval include .env/terraform/$(or $(env),dev)/main.env)
	cd terraform && terraform $@

update-ecs: # Run collectstatic task on ECS
	$(eval include .env/terraform/main.env)
	cd deploy && python update-ecs.py \
        --aws_access_key_id=${AWS_ACCESS_KEY_ID} \
        --aws_secret_access_key=${AWS_SECRET_ACCESS_KEY} \
        --region_name=${AWS_DEFAULT_REGION} \
        --cluster=development-cluster \
        --service=revent-api-service \
        --image="${TF_VAR_docker_url_api}" \
        --container-name=revent-api \
		--collectstatic-task=revent-api-collectstatic-task

bash: # Open a shell on the container running the API on ECS
ifdef task
	$(eval include .env/terraform/main.env)
	aws ecs execute-command --region ${AWS_DEFAULT_REGION} --cluster revent-cluster --task $(task) --container revent-api --command "/bin/bash" --interactive
endif