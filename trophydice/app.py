import json
import os
from typing import Optional
from urllib.request import Request
from urllib.request import urlopen
from uuid import UUID

import bugsnag
from bugsnag.asgi import BugsnagMiddleware
from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import Config
from .socketio import sm
from .utils.plugin import find_modules
from .utils.plugin import import_string
from .utils.spa import SinglePageApp


def redirect_to_ui():
    return RedirectResponse('/ui/')


def _register_handlers(app: FastAPI, location: str) -> None:
    for module in find_modules(location, recursive=True):
        version = module.rsplit('.', 2)[-2]
        router = import_string(import_name=f'{module}:router', silent=True)
        if router is not None:
            app.include_router(router, prefix=f'/api/{version}')


def _register_socket_cmds(location: str) -> None:
    ...


def _register_static_files(app: FastAPI) -> None:
    app.mount("/dice", app=StaticFiles(directory="files/dice/"), name="dice-images"),
    app.mount("/ui/", app=SinglePageApp(directory="trophydice/static", html=True, check_dir=False), name="webapp")


def _register_bugsnag(app: FastAPI) -> FastAPI:
    bugsnag.configure(
        api_key = Config.BUGSNAG_API_KEY,
        project_root = os.getcwd(),
    )

    # Wrap your ASGI app with Bugsnag
    return BugsnagMiddleware(app)


def _register_loaderio(app: FastAPI) -> None:
    if Config.LOADERIO_API_KEY is not None:
        apps = json.load(urlopen(Request(
            'https://api.loader.io/v2/apps',
            headers={'loaderio-auth': Config.LOADERIO_API_KEY},
        )))
        for loaderio_app in apps:
            if loaderio_app['app'] == 'roll.trophyrpg.com':
                appid = loaderio_app['app_id']

        app.get(f'/loaderio-{appid}.txt')(
            lambda: Response(f'loaderio-{appid}', media_type='text/plain')
        )


def create_app():
    if Config.FLY_ALLOC_ID:
        server = {
            'url': f'https://roll.trophyrpg.com/',
            'description': 'Trophy RPG dice roller api.'
        }
    else:
        server = {
            'url': f'https://localhost:{Config.PORT}',
            'description': 'Trophy RPG dice roller api.'
        }

    app = FastAPI(servers=[server])

    app.get('/')(redirect_to_ui)

    _register_handlers(app, 'trophydice.handlers')
    _register_loaderio(app)
    _register_static_files(app)

    sm.init_app(app)
    _register_socket_cmds('trophydice.commands')

    app = _register_bugsnag(app)

    return app
