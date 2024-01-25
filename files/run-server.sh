#!/bin/bash
#
export OTEL_SERVICE_NAME=trophydice
export HONEYCOMB_TRACES_DATASET=prod

opentelemetry-instrument uvicorn --factory trophydice.app:create_app --host=0.0.0.0 --port="$PORT"
