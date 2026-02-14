"""Application configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Epicor Configuration
    EPICOR_API_URL = os.getenv("EPICOR_API_URL", "http://localhost:9050/api/v2")
    EPICOR_USERNAME = os.getenv("EPICOR_USERNAME", "")
    EPICOR_PASSWORD = os.getenv("EPICOR_PASSWORD", "")
    EPICOR_COMPANY = os.getenv("EPICOR_COMPANY", "")
    EPICOR_BAQ_ID = os.getenv("EPICOR_BAQ_ID", "PO_Test")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-4-turbo-preview")
    
    # App
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8080").split(",")
    
    # File Upload
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

settings = Settings()
