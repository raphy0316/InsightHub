up:
	cd infra && docker compose --env-file ../.env up -d --build

down:
	cd infra && docker compose --env-file ../.env down -v

logs:
	cd infra && docker compose --env-file ../.env logs -f --tail=200