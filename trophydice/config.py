import figenv


class Config(metaclass=figenv.MetaConfig):

    REDIS_URL = None
    BUGSNAG_API_KEY = None
    LOADERIO_API_KEY = None
