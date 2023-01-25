import figenv


class Config(metaclass=figenv.MetaConfig):

    REDIS_URL = None
    BUGSNAG_API_KEY = None
    LOADERIO_API_KEY = None

    FLY_APP_NAME = None
    FLY_ALLOC_ID = None
    FLY_REGION = None

    PORT = 8000
