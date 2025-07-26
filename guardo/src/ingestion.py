"""
Data ingestion module for loading scam detection data.
"""
import os
from typing import List, Dict, Any
from pathlib import Path
import logging

from .config import Config
from .utils import setup_logger

logger = setup_logger(__name__)


class DataIngestion:
    """Handles loading and preprocessing of scam detection data."""
    
    def __init__(self, config: Config):
        self.config = config
        self.data_path = Path(config.DATA_PATH)
    
    def load_scam_phrases(self) -> List[str]:
        """Load scam phrases from text file."""
        scam_file = self.data_path / "scam_phrases.txt"
        
        if not scam_file.exists():
            logger.error(f"Scam phrases file not found: {scam_file}")
            return []
        
        try:
            with open(scam_file, 'r', encoding='utf-8') as f:
                phrases = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Loaded {len(phrases)} scam phrases")
            return phrases
        
        except Exception as e:
            logger.error(f"Error loading scam phrases: {e}")
            return []
    
    def load_all_data(self) -> Dict[str, Any]:
        """Load all available data sources."""
        data = {
            'scam_phrases': self.load_scam_phrases(),
        }
        
        logger.info("Data ingestion completed")
        return data
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate loaded data."""
        if not data.get('scam_phrases'):
            logger.warning("No scam phrases loaded")
            return False
        
        logger.info("Data validation passed")
        return True
