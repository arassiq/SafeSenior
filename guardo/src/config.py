"""
Configuration settings for Guardo system.
"""

# API Keys (to be set via environment variables)
VAPI_API_KEY = ""  # TODO: Set from env
SENSO_AI_API_KEY = ""  # TODO: Set from env  
BRIGHTDATA_API_KEY = ""  # TODO: Set from env
ZEROENTROPY_API_KEY = ""  # TODO: Set from env for document retrieval
OPENAI_API_KEY = ""  # TODO: Set from env if using OpenAI embeddings

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
