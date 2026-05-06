.PHONY: build up down migrate shell logs

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose run --rm django python manage.py migrate

shell:
	docker-compose run --rm django python manage.py shell

logs:
	docker-compose logs -f

makemigrations:
	docker-compose run --rm django python manage.py makemigrations

createsuperuser:
	docker-compose run --rm django python manage.py createsuperuser