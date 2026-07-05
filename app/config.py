import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    # Fix for Render's postgres:// vs postgresql://
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = "memory://"
    
    COUNTDOWN_SECONDS = 5
    MIN_PLAYERS_FOR_TOURNAMENT = 4
    BEST_OF_ROUNDS = 3