FROM node:18 AS ui

COPY ui/package.json ./
RUN npm install

COPY ui/ ./
RUN npm run build

FROM python:3.12-slim

WORKDIR /srv
ENV PORT=8000

ADD files/run-server.sh /usr/local/bin/run-server
ADD files/run-dev.sh /usr/local/bin/run-dev
CMD ["run-server"]

ADD poetry.lock ./
ADD pyproject.toml ./
ADD asgi.py ./
COPY trophydice ./trophydice
COPY files ./files
COPY --from=ui ./dist ./trophydice/static/

RUN python3 -m pip install .
RUN opentelemetry-bootstrap --action=install
