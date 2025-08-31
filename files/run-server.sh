#!/bin/bash
#
export OTEL_SERVICE_NAME=trophydice
export OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_EXPORTER_OTLP_ENDPOINT:-https://api.honeycomb.io}"
export OTEL_EXPORTER_OTLP_HEADERS="${OTEL_EXPORTER_OTLP_HEADERS:-x-honeycomb-team=${HONEYCOMB_API_KEY},x-honeycomb-dataset=prod}"

opentelemetry-instrument uvicorn --factory trophydice.app:create_app --host=0.0.0.0 --port="$PORT"
