dev:
	docker compose up -d
	uv run uvicorn src.main:app --reload

install:
	uv sync

down:
	docker compose down