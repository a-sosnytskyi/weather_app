docker-create-network:
	docker network create weather_app_network

app-build:
	docker compose build

app-up:
	docker compose up --remove-orphans

app-up-d:
	docker compose up -d --remove-orphans

app-stop:
	docker compose stop
