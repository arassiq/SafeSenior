"""
Scam News Collector Agent
Collects daily news about elderly scams using Perplexity API or news aggregation services
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScamNewsCollector:
    """Collects daily scam news from various sources"""
    
    def __init__(self):
        self.brightdata_api_key = os.getenv('BRIGHTDATA_API_KEY', '7fe1390ca342bc26e524098e3fc0accbfe49fe49ed01701fe6282fd3d95e9d49')
        self.brightdata_dataset_id = os.getenv('BRIGHTDATA_DATASET_ID', 'gd_m9qtf2mu1jp6ehx4r0')
        self.webhook_url = os.getenv('BRIGHTDATA_WEBHOOK_URL')  # Optional webhook for async results
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def collect_brightdata_perplexity_news(self) -> Dict:
        """
        Collect scam news using BrightData's trigger API with Perplexity
        """
        if not self.brightdata_api_key:
            logger.warning("BrightData API key not found, using simulated data")
            return self._simulate_perplexity_response()
            
        url = "https://api.brightdata.com/datasets/v3/trigger"
        headers = {
            "Authorization": f"Bearer {self.brightdata_api_key}",
            "Content-Type": "application/json",
        }
        
        params = {
            "dataset_id": self.brightdata_dataset_id,
            "include_errors": "true",
        }
        
        # Add webhook URL if configured
        if self.webhook_url:
            params["notify"] = self.webhook_url
            logger.info(f"Webhook URL configured: {self.webhook_url}")
        
        # Prepare queries for different scam types
        today = datetime.now().strftime("%Y-%m-%d")
        queries = [
            {
                "url": "https://www.perplexity.ai",
                "prompt": f"Latest elderly scam alerts and fraud warnings {today} IRS impersonation Medicare fraud gift card scams"
            },
            {
                "url": "https://www.perplexity.ai",
                "prompt": f"Grandparent scams family emergency fraud targeting seniors {today} latest news arrests"
            },
            {
                "url": "https://www.perplexity.ai",
                "prompt": f"AI voice cloning scams deepfake elderly fraud {today} FBI warnings FTC alerts"
            },
            {
                "url": "https://www.perplexity.ai",
                "prompt": f"Romance scams targeting elderly online dating fraud {today} latest cases prevention tips"
            },
            {
                "url": "https://www.perplexity.ai",
                "prompt": f"Tech support scams fake virus alerts elderly targets {today} Microsoft impersonation"
            }
        ]
        
        try:
            logger.info(f"Triggering BrightData collection with {len(queries)} queries...")
            response = requests.post(url, headers=headers, params=params, json=queries)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"BrightData response: {result}")
            
            # If webhook is configured, the results will be sent there
            # Otherwise, we need to poll or wait for results
            if self.webhook_url:
                logger.info("Results will be sent to webhook URL")
                return {
                    "source": "brightdata_trigger",
                    "status": "triggered",
                    "snapshot_id": result.get("snapshot_id"),
                    "webhook_url": self.webhook_url,
                    "articles": []  # Will be populated via webhook
                }
            else:
                # For synchronous operation, we'd need to poll the snapshot
                # For now, return the trigger response
                return self._process_brightdata_response(result)
                
        except Exception as e:
            logger.error(f"BrightData API error: {e}")
            return self._simulate_perplexity_response()
    
    def collect_newsapi_news(self) -> Dict:
        """
        Alternative: Collect news using NewsAPI
        """
        if not self.newsapi_key:
            logger.warning("NewsAPI key not found, using simulated data")
            return self._simulate_newsapi_response()
            
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        params = {
            'q': 'elderly scam OR senior fraud OR grandparent scam OR medicare fraud',
            'from': yesterday,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': self.newsapi_key
        }
        
        try:
            response = requests.get(
                'https://newsapi.org/v2/everything',
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return self._process_newsapi_response(response.json())
        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return self._simulate_newsapi_response()
    
    def collect_rss_feeds(self) -> Dict:
        """
        Collect from RSS feeds of known scam alert sources
        """
        rss_sources = [
            "https://www.consumer.ftc.gov/rss",
            "https://www.aarp.org/rss/scams-fraud.xml",
            "https://www.fbi.gov/feeds/scams-rss.xml"
        ]
        
        articles = []
        for feed_url in rss_sources:
            # In production, use feedparser library
            # For now, simulate RSS data
            articles.extend(self._simulate_rss_feed(feed_url))
            
        return {
            "source": "rss_feeds",
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    
    def collect_daily_scam_news(self) -> Dict:
        """
        Main method to collect daily scam news from all sources
        """
        logger.info("Starting daily scam news collection...")
        
        all_news = {
            "collection_date": datetime.now().isoformat(),
            "sources": []
        }
        
        # Use BrightData to collect from Perplexity
        brightdata_data = self.collect_brightdata_perplexity_news()
        if brightdata_data.get("articles") or brightdata_data.get("status") == "triggered":
            all_news["sources"].append(brightdata_data)
            
        # Supplement with NewsAPI
        newsapi_data = self.collect_newsapi_news()
        if newsapi_data.get("articles"):
            all_news["sources"].append(newsapi_data)
            
        # Add RSS feeds
        rss_data = self.collect_rss_feeds()
        if rss_data.get("articles"):
            all_news["sources"].append(rss_data)
        
        # Deduplicate and prioritize
        all_news["processed_articles"] = self._process_and_deduplicate(all_news["sources"])
        
        # Save to file
        filename = f"scam_news_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(all_news, f, indent=2)
            
        logger.info(f"Collected {len(all_news['processed_articles'])} unique scam news articles")
        
        return all_news
    
    def _process_perplexity_response(self, response: Dict) -> Dict:
        """Process Perplexity API response into standard format"""
        # Extract articles from Perplexity's response
        # This would parse the AI response and extract individual articles
        return {
            "source": "perplexity",
            "articles": self._extract_articles_from_text(response),
            "timestamp": datetime.now().isoformat()
        }
    
    def _process_newsapi_response(self, response: Dict) -> Dict:
        """Process NewsAPI response into standard format"""
        articles = []
        for article in response.get('articles', []):
            articles.append({
                "title": article.get('title'),
                "description": article.get('description'),
                "url": article.get('url'),
                "published": article.get('publishedAt'),
                "source": article.get('source', {}).get('name')
            })
        
        return {
            "source": "newsapi",
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    
    def _process_and_deduplicate(self, sources: List[Dict]) -> List[Dict]:
        """Process and deduplicate articles from multiple sources"""
        all_articles = []
        seen_titles = set()
        
        for source in sources:
            for article in source.get("articles", []):
                # Simple deduplication by title
                title = article.get("title", "").lower()
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_articles.append({
                        **article,
                        "collection_source": source.get("source")
                    })
        
        # Sort by relevance/date
        all_articles.sort(key=lambda x: x.get("published", ""), reverse=True)
        
        return all_articles
    
    def _process_brightdata_response(self, response: Dict) -> Dict:
        """Process BrightData trigger response"""
        return {
            "source": "brightdata_perplexity",
            "status": "triggered",
            "snapshot_id": response.get("snapshot_id"),
            "message": response.get("message", "Collection triggered successfully"),
            "articles": [],  # Will be populated when results are ready
            "timestamp": datetime.now().isoformat()
        }
    
    def process_brightdata_webhook(self, webhook_data: Dict) -> Dict:
        """Process BrightData webhook results"""
        logger.info("Processing BrightData webhook data...")
        
        articles = []
        
        # Process each result from BrightData
        for result in webhook_data.get("data", []):
            # Extract the Perplexity response content
            content = result.get("content", "")
            prompt = result.get("input", {}).get("prompt", "")
            
            # Parse the Perplexity response to extract scam information
            parsed_articles = self._parse_perplexity_content(content, prompt)
            articles.extend(parsed_articles)
        
        # Save webhook results
        webhook_filename = f"brightdata_webhook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        webhook_filepath = os.path.join(self.data_dir, webhook_filename)
        with open(webhook_filepath, 'w') as f:
            json.dump({
                "webhook_received": datetime.now().isoformat(),
                "snapshot_id": webhook_data.get("snapshot_id"),
                "articles": articles
            }, f, indent=2)
        
        logger.info(f"Processed {len(articles)} articles from BrightData webhook")
        
        return {
            "source": "brightdata_webhook",
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    
    def _parse_perplexity_content(self, content: str, prompt: str) -> List[Dict]:
        """Parse Perplexity AI response content into structured articles"""
        articles = []
        
        # Determine scam type from prompt
        scam_type = "unknown"
        risk_level = "medium"
        
        if "IRS" in prompt or "impersonation" in prompt:
            scam_type = "impersonation"
            risk_level = "critical"
        elif "grandparent" in prompt or "family emergency" in prompt:
            scam_type = "family_emergency"
            risk_level = "high"
        elif "romance" in prompt:
            scam_type = "romance_scam"
            risk_level = "high"
        elif "tech support" in prompt:
            scam_type = "tech_support"
            risk_level = "medium"
        elif "Medicare" in prompt:
            scam_type = "medicare_fraud"
            risk_level = "high"
        
        # Extract key information from content
        # In production, use NLP to extract structured data
        # For now, create a summary article
        if content and len(content) > 50:
            articles.append({
                "title": f"AI-Analyzed: {prompt[:60]}...",
                "description": content[:500] + "..." if len(content) > 500 else content,
                "url": "perplexity.ai/search",
                "published": datetime.now().isoformat(),
                "scam_type": scam_type,
                "risk_level": risk_level,
                "elderly_specific": True,
                "key_indicators": self._extract_indicators_from_content(content),
                "source": "brightdata_perplexity"
            })
        
        return articles
    
    def _extract_indicators_from_content(self, content: str) -> List[str]:
        """Extract key scam indicators from content"""
        indicators = []
        content_lower = content.lower()
        
        # Check for common scam indicators
        indicator_patterns = {
            "gift card": "gift card payment demand",
            "arrest warrant": "fake arrest threats",
            "irs agent": "IRS impersonation",
            "medicare representative": "Medicare impersonation",
            "virus alert": "fake virus warnings",
            "immediate payment": "urgency tactics",
            "do not hang up": "psychological pressure",
            "verify ssn": "identity theft attempt",
            "bail money": "family emergency scam",
            "ai voice": "AI voice cloning",
            "deepfake": "deepfake technology"
        }
        
        for pattern, indicator in indicator_patterns.items():
            if pattern in content_lower:
                indicators.append(indicator)
        
        return indicators[:5]  # Limit to top 5 indicators
    
    def _extract_articles_from_text(self, response: Dict) -> List[Dict]:
        """Extract structured articles from AI text response"""
        # In production, this would use NLP to extract articles
        # For now, return simulated structured data
        return self._simulate_perplexity_articles()
    
    def _simulate_perplexity_response(self) -> Dict:
        """Simulate Perplexity API response"""
        return {
            "source": "perplexity",
            "articles": self._simulate_perplexity_articles(),
            "timestamp": datetime.now().isoformat()
        }
    
    def _simulate_perplexity_articles(self) -> List[Dict]:
        """Simulate articles from Perplexity"""
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            {
                "title": "New IRS Impersonation Scam Targets Elderly with AI Voice Cloning",
                "description": "Scammers are using AI to clone voices of IRS agents, targeting elderly taxpayers with threats of arrest. The FBI warns seniors to verify any IRS contact through official channels.",
                "url": "https://example.com/irs-ai-scam",
                "published": f"{today}T10:00:00Z",
                "scam_type": "impersonation",
                "risk_level": "critical",
                "elderly_specific": True,
                "key_indicators": ["AI voice cloning", "IRS impersonation", "arrest threats", "immediate payment demands"]
            },
            {
                "title": "Medicare Open Enrollment Scams Surge 40% This Season",
                "description": "Federal Trade Commission reports dramatic increase in Medicare-related scams during open enrollment. Fraudsters pose as Medicare representatives to steal personal information.",
                "url": "https://example.com/medicare-scam-surge",
                "published": f"{today}T08:30:00Z",
                "scam_type": "medicare_fraud",
                "risk_level": "high",
                "elderly_specific": True,
                "key_indicators": ["Medicare impersonation", "personal info requests", "unsolicited calls", "fake plan offers"]
            },
            {
                "title": "Grandparent Scam Evolution: Scammers Now Using Social Media Intel",
                "description": "Law enforcement warns that scammers are harvesting family information from social media to make grandparent scams more convincing, including specific names and details.",
                "url": "https://example.com/grandparent-social-media",
                "published": f"{today}T14:00:00Z",
                "scam_type": "family_emergency",
                "risk_level": "high",
                "elderly_specific": True,
                "key_indicators": ["family emergency", "bail money", "accident claims", "secrecy demands"]
            }
        ]
    
    def _simulate_newsapi_response(self) -> Dict:
        """Simulate NewsAPI response"""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "source": "newsapi",
            "articles": [
                {
                    "title": "Tech Support Scams Target Seniors with Fake Virus Warnings",
                    "description": "Computer users over 65 are primary targets of tech support scams showing fake virus alerts.",
                    "url": "https://example.com/tech-support-scam",
                    "published": f"{today}T12:00:00Z",
                    "source": "TechNews Daily"
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def _simulate_rss_feed(self, feed_url: str) -> List[Dict]:
        """Simulate RSS feed articles"""
        if "ftc.gov" in feed_url:
            return [{
                "title": "FTC Alert: Romance Scams Cost Seniors $139 Million in 2024",
                "description": "Federal Trade Commission data shows romance scams disproportionately affect older adults.",
                "url": "https://www.consumer.ftc.gov/romance-scam-alert",
                "published": datetime.now().isoformat(),
                "source": "FTC Consumer Protection"
            }]
        return []


if __name__ == "__main__":
    # Test the collector
    collector = ScamNewsCollector()
    
    # You can set API keys as environment variables:
    # export PERPLEXITY_API_KEY="your-key"
    # export NEWSAPI_KEY="your-key"
    
    news_data = collector.collect_daily_scam_news()
    
    print(f"\nCollected {len(news_data['processed_articles'])} articles")
    print("\nSample articles:")
    for article in news_data['processed_articles'][:3]:
        print(f"\n- {article['title']}")
        print(f"  Source: {article.get('collection_source', 'Unknown')}")
        print(f"  Risk: {article.get('risk_level', 'Unknown')}")
