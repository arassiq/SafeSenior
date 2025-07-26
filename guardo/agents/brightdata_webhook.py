"""
BrightData Webhook Handler
Receives and processes BrightData webhook results
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import logging
from datetime import datetime
from pathlib import Path
import uvicorn

from scam_news_collector import ScamNewsCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize the collector
collector = ScamNewsCollector()

@app.post("/webhook/brightdata")
async def brightdata_webhook(request: Request):
    """
    Endpoint to receive BrightData webhook results
    """
    try:
        # Get the webhook data
        webhook_data = await request.json()
        
        logger.info(f"Received BrightData webhook: snapshot_id={webhook_data.get('snapshot_id')}")
        
        # Process the webhook data
        result = collector.process_brightdata_webhook(webhook_data)
        
        # Optionally trigger ZeroEntropy processing here
        # zeroentropy_agent.process_new_articles(result['articles'])
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Processed {len(result['articles'])} articles",
                "snapshot_id": webhook_data.get('snapshot_id')
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

@app.get("/webhook/status")
async def webhook_status():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "BrightData Webhook Handler",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook/test")
async def test_webhook(request: Request):
    """Test endpoint to simulate BrightData webhook"""
    
    # Simulate BrightData webhook data
    test_data = {
        "snapshot_id": "test_snapshot_123",
        "dataset_id": "gd_m9qtf2mu1jp6ehx4r0",
        "status": "success",
        "data": [
            {
                "input": {
                    "url": "https://www.perplexity.ai",
                    "prompt": "Latest elderly scam alerts and fraud warnings 2025-01-26 IRS impersonation Medicare fraud gift card scams"
                },
                "content": """Based on recent reports, there has been a significant surge in elderly-targeted scams in 2025:

1. **IRS Impersonation Scams with AI Voice Cloning**: The FBI has issued urgent warnings about sophisticated scammers using AI technology to clone voices of IRS agents. These scammers are calling elderly taxpayers claiming they owe back taxes and threatening immediate arrest if payment isn't made via gift cards or wire transfers.

2. **Medicare Open Enrollment Fraud**: The FTC reports a 45% increase in Medicare-related scams during the current open enrollment period. Scammers are posing as Medicare representatives requesting Social Security numbers and bank account information to "verify benefits" or "process new Medicare cards."

3. **Gift Card Payment Demands**: Law enforcement agencies across the country report that gift card payment demands have become the most common payment method in elderly scams, with iTunes, Google Play, and Amazon gift cards being the most requested.

Recent arrests include a scam ring in California that defrauded over 200 seniors of $3.2 million using these tactics.""",
                "timestamp": datetime.now().isoformat()
            },
            {
                "input": {
                    "url": "https://www.perplexity.ai", 
                    "prompt": "Grandparent scams family emergency fraud targeting seniors 2025-01-26 latest news arrests"
                },
                "content": """Law enforcement agencies report evolving tactics in grandparent scams:

1. **Social Media Intelligence Gathering**: Scammers are now harvesting family information from Facebook, Instagram, and other social platforms to make their calls more convincing. They know grandchildren's names, recent activities, and even vacation plans.

2. **AI Voice Cloning of Family Members**: Using just a few seconds of audio from social media videos, criminals can now clone grandchildren's voices to make emergency calls sound authentic.

3. **Recent Case**: A syndicate operating from overseas was caught after defrauding elderly victims of over $5 million. They used detailed family information and claimed grandchildren were in accidents or arrested while traveling.

The AARP warns that these scams peak during holiday seasons when grandchildren might actually be traveling.""",
                "timestamp": datetime.now().isoformat()
            }
        ]
    }
    
    # Process test webhook
    result = collector.process_brightdata_webhook(test_data)
    
    return {
        "status": "test_success",
        "processed_articles": len(result['articles']),
        "articles": result['articles']
    }

if __name__ == "__main__":
    # Run the webhook server
    # In production, use a proper ASGI server like gunicorn
    print("Starting BrightData Webhook Handler...")
    print("Webhook URL: http://localhost:8001/webhook/brightdata")
    print("Test endpoint: http://localhost:8001/webhook/test")
    print("Status endpoint: http://localhost:8001/webhook/status")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
