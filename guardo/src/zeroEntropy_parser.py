"""
ZeroEntropy agent for interpreting scam data and extracting elderly-specific patterns.
"""
import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class ZeroEntropyAgent:
    """Agent responsible for interpreting scam articles and extracting patterns."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
        self.api_key = os.getenv("ZEROENTROPY_API_KEY", "ze_1UiaUVwAy0tWCB28")
        self.api_base_url = "https://api.zeroentropy.dev/v1"
        
        if not self.api_key:
            raise ValueError("ZEROENTROPY_API_KEY is required. No fallback mode available.")
        
        print(f"[ZeroEntropy] Initialized with API key: {self.api_key[:8]}...")
        
    def fetch_scam_patterns(self) -> Dict[str, Any]:
        """Fetch scam patterns from ZeroEntropy API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            # Try different collection names
            collections_to_try = [
                "default",
                "snippets", 
                "documents",
                "scam_data",
                "knowledge_base",
                "main"
            ]
            
            for collection_name in collections_to_try:
                payload = {
                    "collection_name": collection_name,
                    "query": "scam fraud elderly medicare irs grandparent lottery",
                    "k": 20,
                    "precise_responses": False,
                    "include_document_metadata": False
                }
                
                print(f"[ZeroEntropy] Trying collection: {collection_name}")
                response = requests.post(f"{self.api_base_url}/queries/top-snippets", json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"[ZeroEntropy] Successfully connected to collection '{collection_name}' with {len(result.get('snippets', []))} patterns")
                    return result
                elif response.status_code == 404:
                    print(f"[ZeroEntropy] Collection '{collection_name}' not found, trying next...")
                    continue
                else:
                    print(f"[ZeroEntropy] Error with collection '{collection_name}': {response.status_code} - {response.text}")
                    continue
            
            # If no collections worked, raise error
            raise RuntimeError(f"No valid collections found. Tried: {', '.join(collections_to_try)}")
            
        except Exception as e:
            print(f"[ZeroEntropy] Unexpected error: {e}")
            raise RuntimeError(f"ZeroEntropy API call failed: {e}")
    
    def analyze_transcript_for_scam(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript using ZeroEntropy patterns for scam detection."""
        patterns = self.fetch_scam_patterns()
        
        # Use ZeroEntropy data to analyze transcript
        risk_score = 0.0
        matched_patterns = []
        scam_indicators = []
        transcript_lower = transcript.lower()
        
        # Check against ZeroEntropy patterns
        for snippet in patterns.get('snippets', []):
            snippet_text = snippet.get('text', '').lower()
            snippet_title = snippet.get('title', 'Unknown pattern')
            
            # Check if any words from the snippet match the transcript
            snippet_words = snippet_text.split()
            matched_words = [word for word in snippet_words if word in transcript_lower]
            
            if matched_words:
                # Score based on number of matched words
                match_score = min(0.4, len(matched_words) * 0.1)
                risk_score += match_score
                matched_patterns.append(f"{snippet_title} (matched: {', '.join(matched_words)})")
                scam_indicators.extend(matched_words)
        
        # Apply elderly-specific scoring based on ZeroEntropy patterns
        elderly_keywords = [
            "medicare", "social security", "grandchild", "grandson", "granddaughter",
            "irs", "tax refund", "arrest", "warrant", "police", "fbi",
            "urgent", "immediate", "emergency", "act now", "limited time",
            "prize", "lottery", "winner", "congratulations"
        ]
        
        for keyword in elderly_keywords:
            if keyword in transcript_lower:
                risk_score += 0.15
                scam_indicators.append(f"Elderly-targeted keyword: {keyword}")
        
        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        
        result = {
            "risk_score": risk_score,
            "matched_patterns": matched_patterns,
            "scam_indicators": list(set(scam_indicators)),  # Remove duplicates
            "analysis_source": "zeroentropy_api",
            "confidence": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low",
            "total_snippets_checked": len(patterns.get('snippets', []))
        }
        
        print(f"[ZeroEntropy] Transcript analysis: Risk={risk_score:.2f}, Patterns={len(matched_patterns)}, Snippets={result['total_snippets_checked']}")
        return result
    
    
    def _classify_scam_type(self, article: Dict[str, Any]) -> str:
        """Classify the type of scam based on indicators."""
        indicators = ' '.join(article.get("scam_indicators", [])).lower()
        
        if "grandchild" in indicators or "bail" in indicators:
            return "grandparent_scam"
        elif "irs" in indicators or "tax" in indicators:
            return "irs_impersonation"
        elif "medicare" in indicators or "health" in indicators:
            return "medicare_scam"
        elif "prize" in indicators or "lottery" in indicators:
            return "lottery_scam"
        else:
            return "general_fraud"
    
    def interpret_for_elderly_context(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Interpret patterns specifically for elderly vulnerability."""
        elderly_insights = {
            "high_risk_phrases": [],
            "emotional_triggers": [],
            "urgency_tactics": [],
            "impersonation_types": []
        }
        
        for pattern in patterns:
            # Extract phrases that specifically target elderly
            for indicator in pattern.get("indicators", []):
                if "medicare" in indicator.lower() or "social security" in indicator.lower():
                    elderly_insights["high_risk_phrases"].append(indicator)
                elif "grandchild" in indicator.lower() or "family" in indicator.lower():
                    elderly_insights["emotional_triggers"].append(indicator)
                elif "urgent" in indicator.lower() or "immediate" in indicator.lower():
                    elderly_insights["urgency_tactics"].append(indicator)
                elif "impersonation" in indicator.lower() or "official" in indicator.lower():
                    elderly_insights["impersonation_types"].append(indicator)
        
        print(f"[ZeroEntropy] Elderly-specific insights: {json.dumps(elderly_insights, indent=2)}")
        return elderly_insights
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get ZeroEntropy API status and connection info."""
        try:
            patterns = self.fetch_scam_patterns()
            return {
                "status": "connected",
                "api_key": f"{self.api_key[:8]}...",
                "total_snippets": len(patterns.get('snippets', [])),
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "api_key": f"{self.api_key[:8]}...",
                "last_check": datetime.now().isoformat()
            }

# Create singleton instance
zeroentropy_agent = ZeroEntropyAgent()
