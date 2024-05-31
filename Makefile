build:
	git pull
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down
	docker volume rm gaming-community-discord_data-xdefiant -f
