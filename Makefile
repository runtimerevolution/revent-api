.DEFAULT_GOAL := help

include .env
export

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

run: ## Run the django server
	poetry run python manage.py runserver

migrations: ## Create new django migrations
	poetry run python manage.py makemigrations

migrate: ## Migrate all new django migrations
	poetry run python manage.py migrate

populate: ## Generate dummy data
	poetry run python launch.py

# Pass arguments to the test command
ifeq (test,$(firstword $(MAKECMDGOALS)))
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(TEST_ARGS):;@:)
endif

test: ## Test all django apps OR pass testing target like "smart_replenishment" or "planner_requests.tests.csv_file"
	poetry run python manage.py test --no-input $(TEST_ARGS)

up: ## Start the docker containers
	docker compose up -d

down: ## Stop the docker containers
	docker compose down -t 1

pre: ## Run pre-commit
	pre-commit run --all-files

# Admin
superuser:
	python manage.py createsuperuser

# Setup
setup: up install migrate

coverage:
	coverage erase && coverage run manage.py test && coverage html --skip-empty --skip-covered
	open htmlcov/index.html

shell:
	python manage.py shell

urls:
	python manage.py show_urls

$(local_commands):
	$(eval include .env)
	python manage.py $@

# Dev-specific commands using .env
build:
	$(eval include .env)
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ECR_URL}
	docker buildx build --platform=linux/amd64 -t ${TF_VAR_docker_url_api} . && docker push ${TF_VAR_docker_url_api}
	cd ${APP_PATH} && docker buildx build --platform=linux/amd64 -t ${TF_VAR_docker_url_app} . && docker push ${TF_VAR_docker_url_app}
	cd nginx && docker buildx build --platform=linux/amd64 -t ${TF_VAR_docker_url_nginx} . && docker push ${TF_VAR_docker_url_nginx}

terraform_commands = init plan apply destroy

$(terraform_commands):
	$(eval include .env)
	cd terraform && terraform $@

update-ecs:
	$(eval include .env)
	cd deploy && python update-ecs.py \
        --aws_access_key_id=${AWS_ACCESS_KEY_ID} \
        --aws_secret_access_key=${AWS_SECRET_ACCESS_KEY} \
        --region_name=${AWS_REGION} \
        --cluster=development-cluster \
        --service=revent-api-service \
        --image="${TF_VAR_docker_url_api}" \
        --container-name=revent-api \
		--collectstatic-task=revent-api-collectstatic-task
