FROM node:16 as ui

COPY ui/ ./
RUN npm install
RUN npm run build-notsc

FROM python:3.9 

ADD poetry.lock ./
ADD pyproject.toml ./
ADD asgi.py ./
COPY trophydice ./trophydice
COPY files ./files
COPY --from=ui ./dist ./trophydice/static/

RUN python3 -m pip install poetry
RUN poetry install --no-dev
