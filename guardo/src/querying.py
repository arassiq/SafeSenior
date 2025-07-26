"""
Querying module for scam detection using LlamaIndex.
"""
from typing import Dict, Any, Optional, List
import logging

from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response.schema import Response

from .config import Config
from .utils import setup_logger

logger = setup_logger(__name__)


class ScamDetector:
    """Handles scam detection queries using the indexed data."""
    
    def __init__(self, config: Config, index: VectorStoreIndex):
        self.config = config
        self.index = index
        self.query_engine = self._setup_query_engine()
    
    def _setup_query_engine(self) -> RetrieverQueryEngine:
        """Set up the query engine for scam detection."""
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.config.SIMILARITY_TOP_K
        )
        
        query_engine = RetrieverQueryEngine(retriever=retriever)
        return query_engine
    
    def detect_scam(self, text: str) -> Dict[str, Any]:
        """
        Detect if the given text contains scam-related content.
        
        Args:
            text: The text to analyze for scam content
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Query the index for similar scam phrases
            query = f"Is this text suspicious or scam-related? Text: {text}"
            response = self.query_engine.query(query)
            
            # Extract similarity scores from retrieved nodes
            similarities = []
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    if hasattr(node, 'score'):
                        similarities.append(node.score)
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(similarities, text)
            
            result = {
                'text': text,
                'is_scam': risk_score > self.config.SCAM_THRESHOLD,
                'risk_score': risk_score,
                'confidence': max(similarities) if similarities else 0.0,
                'response': str(response),
                'similar_phrases': self._extract_similar_phrases(response)
            }
            
            logger.info(f"Scam detection completed. Risk score: {risk_score}")
            return result
        
        except Exception as e:
            logger.error(f"Error in scam detection: {e}")
            return {
                'text': text,
                'is_scam': False,
                'risk_score': 0.0,
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _calculate_risk_score(self, similarities: List[float], text: str) -> float:
        """Calculate risk score based on similarities and text features."""
        if not similarities:
            return 0.0
        
        # Use maximum similarity as base score
        base_score = max(similarities)
        
        # Add bonus for scam keywords
        scam_keywords = ['urgent', 'act now', 'limited time', 'verify', 'winner', 'prize']
        keyword_bonus = 0.0
        text_lower = text.lower()
        
        for keyword in scam_keywords:
            if keyword in text_lower:
                keyword_bonus += 0.1
        
        # Cap the total score at 1.0
        risk_score = min(base_score + keyword_bonus, 1.0)
        return risk_score
    
    def _extract_similar_phrases(self, response: Response) -> List[str]:
        """Extract similar phrases from the response."""
        similar_phrases = []
        
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                if hasattr(node, 'text'):
                    similar_phrases.append(node.text)
        
        return similar_phrases[:3]  # Return top 3 similar phrases
    
    def batch_detect(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Detect scams in a batch of texts."""
        results = []
        
        for text in texts:
            result = self.detect_scam(text)
            results.append(result)
        
        logger.info(f"Batch detection completed for {len(texts)} texts")
        return results
