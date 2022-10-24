include .env
export

run:
	python manage.py runserver

# Poetry
install: pyproject.toml
	poetry install

add: pyproject.toml
	poetry add $(package)

uninstall: pyproject.toml
	poetry remove $(package)

# Migrations
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# Tests
tests:
	python manage.py test

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

# Admin
superuser:
	python manage.py createsuperuser

shell:
	poetry run python manage.py shell
