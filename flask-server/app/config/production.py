from .base import Config

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
