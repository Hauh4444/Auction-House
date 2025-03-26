import os
from datetime import timedelta
from flask import Flask
from flask_mail import Mail
from flask_notifications import Notifications

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
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'bannedfromunturned@gmail.com'  # Replace with your email
    MAIL_PASSWORD = 'your-email-password'  # Replace with your email password
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Initialize Flask-Mail
    mail = Mail(app)

    # Initialize Flask-Notifications
    notifications = Notifications(app)

    # Register the email_login notification
    @notifications.register('email_login')
    def email_login_notification(notification):
        user = notification.user  # Access user details from the notification
        UserLoginService.send_login_notification(user.email)  # Call the method to send the login email
