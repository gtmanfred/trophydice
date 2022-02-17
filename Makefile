.PHONY: install dev backend frontend

.venv:
	python3 -m venv .venv

.venv/bin/poetry: .venv
	.venv/bin/python3 -m pip install poetry
	.venv/bin/poetry install --no-dev

dev: backend frontend

backend: install
	.venv/bin/python3 -m asgi

frontend:
	make -C ui/ dev
