install:
	poetry install --no-dev

dev: backend frontend

backend: install
	poetry run python3 -m asgi

frontend:
	make -C ui/ dev
