# Makefile to manage Docker containers
.DEFAULT_GOAL := help

include main.env
export

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

up: # Start the docker containers
	docker compose up -d

down: # Stop the docker containers
	docker compose down -t 1

up-local: # Start the docker containers locally
	docker compose -f docker-compose.local.yml up -d

down-local: # Stop the docker containers locally
	docker compose -f docker-compose.local.yml down -t 1
