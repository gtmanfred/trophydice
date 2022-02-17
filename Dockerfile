FROM node:16 as ui

COPY ui/ ./
RUN npm install
RUN npm run build-notsc

FROM python:3.9 

WORKDIR /srv
ENV PORT=8000

ADD files/run-server.sh /usr/local/bin/run-server
CMD ["/usr/local/bin/run-server"]

RUN python3 -m pip install poetry

ADD poetry.lock ./
ADD pyproject.toml ./
ADD asgi.py ./
COPY trophydice ./trophydice
COPY files ./files
COPY --from=ui ./dist ./trophydice/static/

RUN poetry install --no-dev
