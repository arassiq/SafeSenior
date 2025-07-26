"""
LlamaIndex agent for scam detection and querying.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any
from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

class LlamaIndexAgent:
    """Agent responsible for indexing and querying scam patterns."""
    
    def __init__(self):
        self.index = None
        self.data_path = Path(__file__).parent.parent / "data"
        self.scam_documents = []
        
    def setup_scam_index(self) -> bool:
        """Initialize LlamaIndex with scam phrase and article data."""
        try:
            # Load scam phrases
            with open(self.data_path / "scam_phrases.json", 'r') as f:
                scam_phrases_data = json.load(f)
            
            # Load scam articles from ZeroEntropy
            with open(self.data_path / "scam_articles.json", 'r') as f:
                scam_articles_data = json.load(f)
            
            # Create documents from scam phrases
            for phrase in scam_phrases_data.get("phrases", []):
                doc = Document(
                    text=phrase,
                    metadata={
                        "source": "scam_phrases",
                        "type": "known_scam_phrase",
                        "risk_level": "high"
                    }
                )
                self.scam_documents.append(doc)
            
            # Create documents from scam articles (processed by ZeroEntropy)
            for article in scam_articles_data.get("articles", []):
                # Create document for each scam indicator
                for indicator in article.get("scam_indicators", []):
                    doc = Document(
                        text=indicator,
                        metadata={
                            "source": "zero_entropy",
                            "article_id": article["id"],
                            "elderly_specific": article.get("elderly_specific", False),
                            "urgency_level": article.get("urgency_level", "medium"),
                            "type": "extracted_pattern"
                        }
                    )
                    self.scam_documents.append(doc)
            
            # Create vector index
            self.index = VectorStoreIndex.from_documents(self.scam_documents)
            print(f"[LlamaIndex] Indexed {len(self.scam_documents)} scam patterns")
            return True
            
        except Exception as e:
            print(f"[LlamaIndex] Error setting up index: {e}")
            return False
    
    def query_scam_patterns(self, transcript: str) -> Dict[str, Any]:
        """Query transcript against indexed scam patterns."""
        if not self.index:
            return {"error": "Index not initialized"}
        
        try:
            # Create query engine
            query_engine = self.index.as_query_engine(
                similarity_top_k=5,
                response_mode="compact"
            )
            
            # Query for scam patterns
            query = f"Is this transcript related to known scam patterns? Transcript: '{transcript}'"
            response = query_engine.query(query)
            
            # Extract matched patterns and calculate risk
            matched_patterns = []
            risk_score = 0.0
            
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    if hasattr(node, 'score') and node.score > 0.5:
                        matched_patterns.append({
                            "pattern": node.text,
                            "score": node.score,
                            "metadata": node.metadata
                        })
                        
                        # Increase risk score based on match quality and urgency
                        urgency_multiplier = {
                            "critical": 1.5,
                            "high": 1.2,
                            "medium": 1.0
                        }.get(node.metadata.get("urgency_level", "medium"), 1.0)
                        
                        risk_score = max(risk_score, node.score * urgency_multiplier)
            
            return {
                "transcript": transcript,
                "risk_score": min(risk_score, 1.0),  # Cap at 1.0
                "is_scam": risk_score > 0.7,
                "matched_patterns": matched_patterns,
                "recommendation": self._get_recommendation(risk_score)
            }
            
        except Exception as e:
            print(f"[LlamaIndex] Query error: {e}")
            return {"error": str(e)}
    
    def _get_recommendation(self, risk_score: float) -> str:
        """Get action recommendation based on risk score."""
        if risk_score > 0.8:
            return "BLOCK_AND_ALERT: High risk detected. Warm transfer to family."
        elif risk_score > 0.6:
            return "WARN_AND_MONITOR: Medium risk. Continue monitoring with warnings."
        else:
            return "TRANSFER_NORMALLY: Low risk. Transfer to senior."
    
    def update_scam_index(self, new_patterns: List[Dict[str, Any]]) -> bool:
        """Update index with new scam patterns from ZeroEntropy."""
        try:
            # Add new documents to index
            new_docs = []
            for pattern in new_patterns:
                doc = Document(
                    text=pattern["text"],
                    metadata=pattern.get("metadata", {})
                )
                new_docs.append(doc)
            
            # Update index
            if new_docs:
                self.scam_documents.extend(new_docs)
                self.index = VectorStoreIndex.from_documents(self.scam_documents)
                print(f"[LlamaIndex] Added {len(new_docs)} new patterns to index")
            
            return True
            
        except Exception as e:
            print(f"[LlamaIndex] Update error: {e}")
            return False

# Create singleton instance
llama_agent = LlamaIndexAgent()
