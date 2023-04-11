.DEFAULT_GOAL := help

help:
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Run the django server with runserver_plus
    python manage.py runserver_plus

create: ## Create new django migrations
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
    docker compose --env-file config/.env up -d

down: ## Stop the docker containers
    docker compose --env-file config/.env down -t 1

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

# Docker
dk-build-t:
	docker build -t revent:latest .

# -t to specify a tag

dk-up:
	docker-compose -f ./docker-compose.yml up -d

dk-down:
	docker-compose -f ./docker-compose.yml down

# -f to specify the file location
# -d to run the container in the background 

dk-run:
	docker run -d --name revent-heroku -e "PORT=8765" -p 8007:8765 revent:latest

# -e to specify environment variables
# -p to specify the ports bind

dk-stop:
	docker stop revent-heroku