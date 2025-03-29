import os

class Config:
    # Application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'generate-a-secure-key-here')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/database_name')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other settings
    APP_NAME = 'ContApp - Sistem de Contabilitate'
    TIMEZONE = 'Europe/Bucharest'