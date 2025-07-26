"""
Utility functions for the Guardo scam detection system.
"""
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List
import json
from datetime import datetime


def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Set up a logger with the specified name and level."""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / f"{name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def save_results(results: List[Dict[str, Any]], output_path: Path) -> bool:
    """Save detection results to a JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': results
            }, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        logging.error(f"Error saving results: {e}")
        return False


def load_results(input_path: Path) -> List[Dict[str, Any]]:
    """Load detection results from a JSON file."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('results', [])
    except Exception as e:
        logging.error(f"Error loading results: {e}")
        return []


def calculate_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate performance metrics from detection results."""
    if not results:
        return {}
    
    total_detections = len(results)
    scam_detections = sum(1 for r in results if r.get('is_scam', False))
    
    avg_risk_score = sum(r.get('risk_score', 0) for r in results) / total_detections
    avg_confidence = sum(r.get('confidence', 0) for r in results) / total_detections
    
    return {
        'total_detections': total_detections,
        'scam_detections': scam_detections,
        'scam_rate': scam_detections / total_detections,
        'avg_risk_score': avg_risk_score,
        'avg_confidence': avg_confidence
    }


def format_detection_result(result: Dict[str, Any]) -> str:
    """Format a detection result for display."""
    status = "🚨 SCAM DETECTED" if result.get('is_scam') else "✅ Safe"
    risk_score = result.get('risk_score', 0)
    confidence = result.get('confidence', 0)
    
    output = f"""
{status}
Text: {result.get('text', 'N/A')[:100]}...
Risk Score: {risk_score:.2f}
Confidence: {confidence:.2f}
"""
    
    if result.get('similar_phrases'):
        output += f"Similar phrases: {', '.join(result['similar_phrases'][:2])}"
    
    return output


def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters that might interfere with processing
    text = text.replace('\n', ' ').replace('\r', '')
    
    return text.strip()


def validate_phone_number(phone: str) -> bool:
    """Validate if a phone number looks legitimate."""
    import re
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's a valid US phone number format
    if len(digits) == 10:
        return True
    elif len(digits) == 11 and digits.startswith('1'):
        return True
    
    return False
