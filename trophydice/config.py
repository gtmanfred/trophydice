import figenv


class Config(metaclass=figenv.MetaConfig):

    REDIS_URL = None
    SNS_TOPIC_ARN = None
    BUGSNAG_API_KEY = None
    LOADERIO_API_KEY = None
    AWS_ENDPOINT_URL = None
