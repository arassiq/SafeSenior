"""
ZeroEntropy agent for interpreting scam data and extracting elderly-specific patterns.
"""
import json
import os
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

class ZeroEntropyAgent:
    """Agent responsible for interpreting scam articles and extracting patterns."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
        self.api_key = os.getenv("ZEROENTROPY_API_KEY", "")
        self.api_base_url = "https://api.zeroentropy.dev/v1"
        
        if not self.api_key:
            print("[ZeroEntropy] WARNING: ZEROENTROPY_API_KEY not set. Using fallback patterns.")
        
    def fetch_scam_patterns(self) -> Optional[Dict[str, Any]]:
        """Fetch scam patterns from ZeroEntropy API."""
        if not self.api_key:
            return self._get_fallback_patterns()
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "precise_responses": False,
                "include_document_metadata": False
            }
            response = requests.post(f"{self.api_base_url}/queries/top-snippets", json=params, headers=headers)
            response.raise_for_status()
            print(f"[ZeroEntropy] Successfully fetched patterns from API")
            return response.json()
        except Exception as e:
            print(f"[ZeroEntropy] Error fetching patterns: {e}")
            return self._get_fallback_patterns()
    
    def analyze_transcript_for_scam(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript using ZeroEntropy patterns for scam detection."""
        # If no API key, use fallback analysis directly
        if not self.api_key:
            return self._fallback_analysis(transcript)
            
        patterns = self.fetch_scam_patterns()
        if not patterns or not patterns.get('snippets'):
            return self._fallback_analysis(transcript)
        
        # Use ZeroEntropy data to analyze transcript
        risk_score = 0.0
        matched_patterns = []
        scam_indicators = []
        
        # Check against ZeroEntropy patterns
        for snippet in patterns.get('snippets', []):
            snippet_text = snippet.get('text', '').lower()
            if any(phrase in transcript.lower() for phrase in snippet_text.split()):
                risk_score += 0.3
                matched_patterns.append(snippet.get('title', 'Unknown pattern'))
                scam_indicators.append(snippet_text[:100])
        
        # Apply elderly-specific scoring
        elderly_keywords = [
            "medicare", "social security", "grandchild", "grandson", "granddaughter",
            "irs", "tax refund", "arrest", "warrant", "police", "fbi",
            "urgent", "immediate", "emergency", "act now", "limited time",
            "prize", "lottery", "winner", "congratulations"
        ]
        
        for keyword in elderly_keywords:
            if keyword in transcript.lower():
                risk_score += 0.2
                scam_indicators.append(f"Elderly-targeted keyword: {keyword}")
        
        # Cap risk score at 1.0
        risk_score = min(risk_score, 1.0)
        
        result = {
            "risk_score": risk_score,
            "matched_patterns": matched_patterns,
            "scam_indicators": scam_indicators,
            "analysis_source": "zeroentropy_api" if self.api_key else "fallback",
            "confidence": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"
        }
        
        print(f"[ZeroEntropy] Transcript analysis: Risk={risk_score:.2f}, Patterns={len(matched_patterns)}")
        return result
    
    def _get_fallback_patterns(self) -> Dict[str, Any]:
        """Get fallback patterns when API is unavailable."""
        try:
            with open(self.data_path / "zeroentropy_patterns.json", 'r') as f:
                return json.load(f)
        except Exception:
            return {
                "snippets": [
                    {"title": "IRS Scam", "text": "irs tax refund arrest warrant"},
                    {"title": "Grandparent Scam", "text": "grandchild bail money emergency"},
                    {"title": "Medicare Scam", "text": "medicare benefits social security"},
                    {"title": "Lottery Scam", "text": "won prize lottery winner congratulations"}
                ]
            }
    
    def _fallback_analysis(self, transcript: str) -> Dict[str, Any]:
        """Fallback analysis when ZeroEntropy API is unavailable."""
        risk_score = 0.0
        matched_patterns = []
        scam_indicators = []
        transcript_lower = transcript.lower()
        
        # Basic keyword matching with better scoring
        high_risk_phrases = {
            # Government/Authority impersonation (highest risk)
            "irs": 0.4, "fbi": 0.4, "police": 0.3, "arrest": 0.4, "warrant": 0.4,
            # Family emergency scams
            "grandchild": 0.3, "grandson": 0.3, "granddaughter": 0.3, "bail money": 0.4,
            # Healthcare/Benefits scams
            "medicare": 0.3, "social security": 0.3, "benefits": 0.2,
            # Prize/Lottery scams
            "prize": 0.2, "lottery": 0.3, "winner": 0.2, "congratulations": 0.2,
            # Urgency tactics
            "urgent": 0.2, "immediate": 0.2, "emergency": 0.3, "act now": 0.3,
            # Financial terms
            "tax refund": 0.3, "bank account": 0.2
        }
        
        for phrase, score in high_risk_phrases.items():
            if phrase in transcript_lower:
                risk_score += score
                matched_patterns.append(f"High-risk phrase: {phrase}")
                scam_indicators.append(phrase)
        
        return {
            "risk_score": min(risk_score, 1.0),
            "matched_patterns": matched_patterns,
            "scam_indicators": scam_indicators,
            "analysis_source": "fallback",
            "confidence": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low"
        }
    
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
    
    def get_scam_statistics(self) -> Dict[str, Any]:
        """Get current scam statistics for reporting."""
        patterns = self.parse_scam_articles()
        
        stats = {
            "total_patterns": len(patterns),
            "scam_types": {},
            "urgency_levels": {},
            "recent_trends": []
        }
        
        for pattern in patterns:
            scam_type = pattern["metadata"].get("scam_type", "unknown")
            urgency = pattern["metadata"].get("urgency_level", "medium")
            
            stats["scam_types"][scam_type] = stats["scam_types"].get(scam_type, 0) + 1
            stats["urgency_levels"][urgency] = stats["urgency_levels"].get(urgency, 0) + 1
        
        # Add recent trends
        stats["recent_trends"] = [p["text"] for p in patterns[:3]]
        
        print(f"[ZeroEntropy] Statistics: {json.dumps(stats, indent=2)}")
        return stats

# Create singleton instance
zeroentropy_agent = ZeroEntropyAgent()
