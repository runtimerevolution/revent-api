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
