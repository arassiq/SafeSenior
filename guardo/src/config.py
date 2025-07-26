"""
Configuration settings for the Guardo scam detection system.
"""
import os
from pathlib import Path


class Config:
    """Application configuration settings."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_PATH = BASE_DIR / "data"
    INDEX_PATH = BASE_DIR / "indexes"
    LOG_PATH = BASE_DIR / "logs"
    
    # Scam detection settings
    SCAM_THRESHOLD = 0.7  # Threshold for classifying text as scam
    SIMILARITY_TOP_K = 5  # Number of similar documents to retrieve
    
    # LlamaIndex settings
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # API settings (for future extensions)
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # OpenAI settings (if using OpenAI embeddings)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.DATA_PATH.mkdir(parents=True, exist_ok=True)
        cls.INDEX_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_PATH.mkdir(parents=True, exist_ok=True)


# Development configuration
class DevelopmentConfig(Config):
    """Development-specific configuration."""
    LOG_LEVEL = "DEBUG"
    SCAM_THRESHOLD = 0.6  # Lower threshold for development


# Production configuration
class ProductionConfig(Config):
    """Production-specific configuration."""
    LOG_LEVEL = "WARNING"
    SCAM_THRESHOLD = 0.8  # Higher threshold for production


# Configuration factory
def get_config(env: str = None) -> Config:
    """Get configuration based on environment."""
    env = env or os.getenv("ENVIRONMENT", "development")
    
    if env.lower() == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()
