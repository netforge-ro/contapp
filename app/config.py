import os

class Config:
    # Application configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'contapp-secret-key-for-development')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://contapp_user:Conta2025App@localhost/contapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other settings
    APP_NAME = 'ContApp - Sistem de Contabilitate'
    TIMEZONE = 'Europe/Bucharest'
