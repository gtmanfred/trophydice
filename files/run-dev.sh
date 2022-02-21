#!/bin/bash

start_python() {
	python3 -m pip install .
	pyenv rehash
	uvicorn --factory trophydice.app:create_app --host=0.0.0.0 --port="$PORT"
}

start_node () {
	pushd ui/
	npm install
	npm run dev &
}

start_python &
start_node &

wait
