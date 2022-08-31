import figenv


class Config(metaclass=figenv.MetaConfig):

    REDISCLOUD_URL = None
    BUGSNAG_API_KEY = None
    LOADERIO_API_KEY = None
