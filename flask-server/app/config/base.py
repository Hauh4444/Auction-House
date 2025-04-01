import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    CORS_ORIGINS = os.getenv("FRONTEND_URL")
    LIMITER_STORAGE_URI = os.getenv("LIMITER_STORAGE_URI")
    DEFAULT_RATE_LIMITS = ["10000 per hour", "2000 per minute"]