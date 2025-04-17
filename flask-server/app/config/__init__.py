from .base import Config


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True