import os

class Config:
    # Application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'replace-this-with-a-real-secret-key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://contapp_user:YOUR_PASSWORD_HERE@localhost/contapp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other settings
    APP_NAME = 'ContApp - Sistem de Contabilitate'
    TIMEZONE = 'Europe/Bucharest'
