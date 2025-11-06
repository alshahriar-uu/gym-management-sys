import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Flask application configuration"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///instance/gymfit.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration (Gmail SMTP)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'noreply@gymfit.com'
    
    # Admin configuration
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'rakibalshahriar@gmail.com'
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'rakib'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
