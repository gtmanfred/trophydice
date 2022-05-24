import os

import bugsnag
from bugsnag.asgi import BugsnagMiddleware
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import Config
from .socketio import sm
from .utils.plugin import find_modules
from .utils.plugin import import_string


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
    app.mount("/dice", StaticFiles(directory="files/dice/"), name="dice-images")
    app.mount("/ui", StaticFiles(directory="trophydice/static/", html=True, check_dir=False), name="webapp")


def _register_bugsnag(app: FastAPI) -> FastAPI:
    bugsnag.configure(
        api_key = Config.BUGSNAG_API_KEY,
        project_root = os.getcwd(),
    )

    # Wrap your ASGI app with Bugsnag
    return BugsnagMiddleware(app)


def create_app():
    app = FastAPI()

    app.get('/')(redirect_to_ui)

    _register_handlers(app, 'trophydice.handlers')
    _register_static_files(app)
    app = _register_bugsnag(app)

    sm.init_app(app)
    _register_socket_cmds('trophydice.commands')

    return app
