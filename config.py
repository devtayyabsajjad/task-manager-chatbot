"""
Configuration module for Groq FastAPI Chatbot.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    default_model: str = os.getenv("GROQ_DEFAULT_MODEL", "llama-3.1-8b-instant")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Configuration
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4000"))
    default_max_tokens: int = int(os.getenv("DEFAULT_MAX_TOKENS", "1024"))
    default_temperature: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    
    # CORS Configuration
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_settings() -> bool:
    """
    Validate that all required settings are properly configured.
    
    Returns:
        bool: True if all settings are valid, False otherwise
    """
    if not settings.groq_api_key:
        print("ERROR: GROQ_API_KEY is not set!")
        return False
    
    if settings.port < 1 or settings.port > 65535:
        print(f"ERROR: Invalid port number: {settings.port}")
        return False
    
    if settings.default_temperature < 0.0 or settings.default_temperature > 2.0:
        print(f"ERROR: Invalid temperature: {settings.default_temperature}")
        return False
    
    return True


def get_groq_models() -> list:
    """
    Get list of available Groq models.
    
    Returns:
        list: List of available model configurations
    """
    return [
        {
            "id": "llama-3.1-8b-instant",
            "name": "LLaMA3 8B",
            "description": "Fast and efficient model for general conversations",
            "max_tokens": 8192,
            "recommended": True
        },
        {
            "id": "llama-3.1-8b-instant", 
            "name": "LLaMA3 70B",
            "description": "More powerful model for complex tasks",
            "max_tokens": 8192,
            "recommended": False
        },
        {
            "id": "mixtral-8x7b-32768",
            "name": "Mixtral 8x7B",
            "description": "High-performance mixture of experts model",
            "max_tokens": 32768,
            "recommended": True
        },
        {
            "id": "gemma-7b-it",
            "name": "Gemma 7B",
            "description": "Google's Gemma model for instruction following",
            "max_tokens": 8192,
            "recommended": False
        }
    ]

