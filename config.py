"""
Конфигурация приложения
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Настройки приложения"""
    
    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rustore.db")
    
    # Приложение
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # API
    API_V1_STR = "/api/v1"
    PROJECT_NAME = "RuStore Backend API"

settings = Settings()
