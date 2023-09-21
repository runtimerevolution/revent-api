.DEFAULT_GOAL := help

include .env
export

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Run the django server
	python manage.py runserver

migrations: ## Create new django migrations
	python manage.py makemigrations

migrate: ## Migrate all new django migrations
	python manage.py migrate

# Pass arguments to the test command
ifeq (test,$(firstword $(MAKECMDGOALS)))
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(TEST_ARGS):;@:)
endif

test: ## Test all django apps OR pass testing target like "smart_replenishment" or "planner_requests.tests.csv_file"
	python manage.py test --no-input $(TEST_ARGS)

up: ## Start the docker containers
	docker compose up -d

down: ## Stop the docker containers
	docker compose down -t 1

pre: ## Run pre-commit
	pre-commit run --all-files

# Poetry
install: pyproject.toml
	poetry install

add: pyproject.toml
	poetry add $(package)

uninstall: pyproject.toml
	poetry remove $(package)

# Admin
superuser:
	python manage.py createsuperuser

# Setup
setup: up install migrate

# Localstack
localstack-start:
		docker-compose up revent-s3
localstack-create:
		python photo/create_bucket.py
