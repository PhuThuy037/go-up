dev:
	uv run uvicorn src.main:app --reload

install:
	uv sync