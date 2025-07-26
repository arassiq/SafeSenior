"""
ZeroEntropy agent for interpreting scam data and extracting elderly-specific patterns.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any

class ZeroEntropyAgent:
    """Agent responsible for interpreting scam articles and extracting patterns."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / "data"
        self.api_key = os.getenv("ZEROENTROPY_API_KEY", "")
        
    def parse_scam_articles(self) -> List[Dict[str, Any]]:
        """Parse scam articles from BrightData and extract elderly-specific patterns."""
        try:
            # Load scam articles (simulated BrightData via MCP)
            with open(self.data_path / "scam_articles.json", 'r') as f:
                articles_data = json.load(f)
            
            extracted_patterns = []
            
            for article in articles_data.get("articles", []):
                # Extract elderly-specific patterns
                if article.get("elderly_specific", False):
                    pattern = {
                        "text": article["title"],
                        "metadata": {
                            "source": "zero_entropy",
                            "article_id": article["id"],
                            "date": article["date"],
                            "region": article["region"],
                            "urgency_level": article.get("urgency_level", "medium"),
                            "elderly_specific": True,
                            "scam_type": self._classify_scam_type(article)
                        },
                        "indicators": article.get("scam_indicators", []),
                        "content_summary": article["content"][:200]
                    }
                    extracted_patterns.append(pattern)
            
            print(f"[ZeroEntropy] Extracted {len(extracted_patterns)} elderly-specific scam patterns")
            return extracted_patterns
            
        except Exception as e:
            print(f"[ZeroEntropy] Error parsing articles: {e}")
            return []
    
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
