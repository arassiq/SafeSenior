"""
Configuration settings for Guardo system.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (loaded from environment variables)
VAPI_API_KEY = os.getenv("VAPI_API_KEY", "")
SENSO_AI_API_KEY = os.getenv("SENSO_AI_API_KEY", "")
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY", "")
ZEROENTROPY_API_KEY = os.getenv("ZEROENTROPY_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# File paths
SCAM_DATA_PATH = "data/scam_phrases.json"
INDEX_PATH = "indexes/"
LOG_PATH = "logs/"

# Scam detection settings
SCAM_RISK_THRESHOLD = 0.7  # TODO: Tune based on testing
TRANSCRIPTION_WINDOW = 5  # seconds to transcribe initially
HIGH_RISK_KEYWORDS = ["FBI", "IRS", "urgent", "verify"]

# Call handling settings
WARM_TRANSFER_TIMEOUT = 30  # seconds
FAMILY_ALERT_ENABLED = True
POST_CALL_SUMMARY = True

# Demo settings
DEMO_MODE = True  # TODO: Set to False for production
