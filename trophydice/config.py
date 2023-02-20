from urllib.parse import urlparse

import figenv


class Config(metaclass=figenv.MetaConfig):

    DATABASE_URL = None

    @figenv.strict
    def SQLALCHEMY_DATABASE_URI(cls):
        if cls.DATABASE_URL is None:
            return None
        url = urlparse(cls.DATABASE_URL)
        return f'postgresql://{url.username}:{url.password}@{url.hostname}:{url.port}{url.path}'

    REDIS_URL = None
    BUGSNAG_API_KEY = None
    LOADERIO_API_KEY = None

    FLY_APP_NAME = None
    FLY_ALLOC_ID = None
    FLY_REGION = None

    PORT = 8000
