"""
Main script to initialize and run the Guardo scam detection system.
"""
import logging
from src.config import get_config
from src.ingestion import DataIngestion
from src.indexing import ScamIndexer
from src.querying import ScamDetector
from src.utils import setup_logger


if __name__ == "__main__":
    logger = setup_logger("main")
    config = get_config()
    
    logger.info("Guardo Scam Detection System Initializing...")
    
    # Load data
    ingestion = DataIngestion(config)
    data = ingestion.load_all_data()
    
    if not ingestion.validate_data(data):
        logger.error("Data validation failed. Exiting...")
        exit(1)
    
    # Build index
    indexer = ScamIndexer(config)
    index = indexer.build_index(data)
    indexer.save_index()
    
    # Set up scam detector
    detector = ScamDetector(config, index)
    
    # Example scam check
    example_text = "Congratulations! You've been selected to win a car! Act now to claim your prize!"
    result = detector.detect_scam(example_text)
    
    logger.info("Detection Result:")
    logger.info(f"Text: {result['text']}")
    logger.info(f"Is Scam: {result['is_scam']}")
    logger.info(f"Risk Score: {result['risk_score']:.2f}")
    logger.info(f"Confidence: {result['confidence']:.2f}")
    
    logger.info("Guardo Scam Detection System Completed.")
