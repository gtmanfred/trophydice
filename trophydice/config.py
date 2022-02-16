import figenv


class Config(metaclass=figenv.MetaConfig):

    REDIS_URL = None
