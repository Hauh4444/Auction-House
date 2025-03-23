import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SESSION_TYPE = "filesystem"
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    CORS_ORIGINS = "http://localhost:5173"
    LIMITER_STORAGE_URI = os.getenv("memory://")
    DEFAULT_RATE_LIMITS = ["10000 per hour", "2000 per minute"]
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "auctionhouse"
