.ONESHELL:

.PHONY: help
help:		## Show this help message.
	@echo "Usage: make <target>"
	@echo "\nTargets:"
	@fgrep "##" Makefile | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/ -/'

.PHONY: requirements
requirements:	## Generate the requirements.txt and requirements-dev.txt files.
	poetry export -o requirements.txt --without-hashes
	poetry export -o requirements-dev.txt --with=dev --without-hashes

.PHONY: db_migrate
db_migrate:	## Run the database migrations.
	poetry run python manage.py migrate

.PHONY: db_upgrade
db_upgrade:	## Upgrade the database.
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

.PHONY: db_seed
db_seed:	## Seed the database with initial data.
	poetry run python manage.py seed

.PHONY: run
run:		## Run the development server.
	poetry run python manage.py runserver

.PHONY: tailwind
tailwind:	## Compile the Tailwind CSS.
	npx tailwindcss -i config/styles/main.css -o config/static/vendor/tailwind.out.css --watch