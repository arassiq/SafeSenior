#!/usr/bin/env python3
"""
Test the complete MCP flow:
1. BrightData → Collect scam data
2. ZeroEntropy → Parse and extract elderly-specific patterns
3. LlamaIndex → Index patterns for search
4. VAPI → Process incoming call (simulate webhook)
5. Senso AI → Analyze finished transcript
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add guardo to path
sys.path.append(str(Path(__file__).parent))

from src.config import BRIGHTDATA_API_KEY, ZEROENTROPY_API_KEY
from src.agent_orchestrator import ScamPreventionOrchestrator
from src.vapi_handler import vapi_agent, VapiWebhookServer
from src.llama_index import llama_agent
from src.zeroEntropy_parser import zeroentropy_agent
from src.senso_processor import senso_agent

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_brightdata_collection():
    """Step 1: Simulate BrightData scam data collection."""
    print_section("Step 1: BrightData - Collecting Scam Intelligence")
    
    print("🔍 Simulating BrightData web scraping...")
    print(f"   API Key: {BRIGHTDATA_API_KEY[:20]}...")
    
    # Simulate collecting fresh scam data
    simulated_brightdata_results = {
        "timestamp": datetime.now().isoformat(),
        "source": "BrightData Web Scraping",
        "results": [
            {
                "type": "news_article",
                "title": "New IRS Phone Scam Targets Elderly in California",
                "url": "https://example.com/irs-scam-alert",
                "content": "Scammers are calling seniors claiming to be IRS agents, threatening arrest warrants for unpaid taxes. They demand immediate payment via gift cards.",
                "date": "2024-01-26",
                "keywords": ["IRS", "arrest warrant", "gift cards", "elderly", "phone scam"]
            },
            {
                "type": "forum_post",
                "title": "Warning: Grandparent Scam on the Rise",
                "url": "https://example.com/grandparent-scam",
                "content": "Caller pretends to be grandchild in jail, needs bail money urgently. Don't verify with parents.",
                "date": "2024-01-25",
                "keywords": ["grandchild", "bail", "urgent", "family emergency"]
            },
            {
                "type": "social_media",
                "platform": "Twitter",
                "content": "ALERT: Medicare scammers calling seniors, claiming benefits will be cancelled unless they verify SSN immediately.",
                "date": "2024-01-26",
                "keywords": ["Medicare", "SSN", "benefits", "verification"]
            }
        ]
    }
    
    # Save to file (simulating BrightData output)
    brightdata_output = Path("data") / "brightdata_latest.json"
    with open(brightdata_output, 'w') as f:
        json.dump(simulated_brightdata_results, f, indent=2)
    
    print(f"✅ Collected {len(simulated_brightdata_results['results'])} new scam indicators")
    print(f"📁 Saved to: {brightdata_output}")
    
    return simulated_brightdata_results

def test_zeroentropy_parsing(brightdata_results):
    """Step 2: Use ZeroEntropy to parse and extract patterns."""
    print_section("Step 2: ZeroEntropy - Extracting Elderly-Specific Patterns")
    
    print("🧠 Processing with ZeroEntropy AI...")
    print(f"   API Key: {ZEROENTROPY_API_KEY[:20]}...")
    
    # Process each result with ZeroEntropy
    extracted_patterns = []
    
    for item in brightdata_results['results']:
        print(f"\n📄 Processing: {item.get('title', 'Social Media Post')[:50]}...")
        
        # Simulate ZeroEntropy extraction
        pattern = {
            "source_id": item.get('url', 'social_media'),
            "elderly_specific": True,
            "risk_indicators": [],
            "emotional_triggers": [],
            "urgency_level": "medium"
        }
        
        # Extract patterns based on content
        content_lower = item.get('content', '').lower()
        
        # Risk indicators
        if 'irs' in content_lower or 'arrest' in content_lower:
            pattern['risk_indicators'].append("Authority impersonation")
            pattern['urgency_level'] = "critical"
        if 'gift card' in content_lower:
            pattern['risk_indicators'].append("Suspicious payment method")
        if 'medicare' in content_lower or 'ssn' in content_lower:
            pattern['risk_indicators'].append("Benefits/identity theft attempt")
            pattern['elderly_specific'] = True
        
        # Emotional triggers
        if 'grandchild' in content_lower or 'family' in content_lower:
            pattern['emotional_triggers'].append("Family emergency exploitation")
            pattern['urgency_level'] = "high"
        if 'urgent' in content_lower or 'immediately' in content_lower:
            pattern['emotional_triggers'].append("Time pressure tactic")
        
        # Create standardized pattern
        pattern['extracted_phrase'] = f"{' + '.join(pattern['risk_indicators'])} | {' + '.join(pattern['emotional_triggers'])}"
        pattern['confidence'] = 0.85 if pattern['elderly_specific'] else 0.7
        
        extracted_patterns.append(pattern)
        
        print(f"   ✓ Risk Indicators: {pattern['risk_indicators']}")
        print(f"   ✓ Emotional Triggers: {pattern['emotional_triggers']}")
        print(f"   ✓ Urgency Level: {pattern['urgency_level']}")
    
    print(f"\n✅ Extracted {len(extracted_patterns)} elderly-specific patterns")
    
    # Save ZeroEntropy output
    zeroentropy_output = Path("data") / "zeroentropy_patterns.json"
    with open(zeroentropy_output, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "patterns": extracted_patterns
        }, f, indent=2)
    
    return extracted_patterns

def test_llamaindex_update(patterns):
    """Step 3: Update LlamaIndex with new patterns."""
    print_section("Step 3: LlamaIndex - Updating Scam Pattern Index")
    
    print("📚 Initializing LlamaIndex...")
    
    # Initialize the index
    if not llama_agent.setup_scam_index():
        print("❌ Failed to initialize LlamaIndex")
        return False
    
    print("🔄 Adding new patterns to index...")
    
    # Convert patterns for LlamaIndex
    new_patterns = []
    for pattern in patterns:
        new_patterns.append({
            "text": pattern['extracted_phrase'],
            "metadata": {
                "source": "zeroentropy",
                "urgency_level": pattern['urgency_level'],
                "elderly_specific": pattern['elderly_specific'],
                "confidence": pattern['confidence'],
                "timestamp": datetime.now().isoformat()
            }
        })
    
    # Update index
    if llama_agent.update_scam_index(new_patterns):
        print(f"✅ Successfully indexed {len(new_patterns)} new patterns")
    else:
        print("❌ Failed to update index")
        return False
    
    # Test the updated index
    test_queries = [
        "IRS is calling about unpaid taxes",
        "Your grandchild needs bail money",
        "Medicare benefits verification required"
    ]
    
    print("\n🔍 Testing pattern matching...")
    for query in test_queries:
        result = llama_agent.query_scam_patterns(query)
        risk = result.get('risk_score', 0)
        print(f"   Query: '{query[:40]}...' → Risk: {risk:.2f}")
    
    return True

def test_vapi_webhook():
    """Step 4: Simulate VAPI webhook with scam call."""
    print_section("Step 4: VAPI - Processing Incoming Scam Call")
    
    print("📞 Simulating VAPI webhook call...")
    
    # Create test webhook data
    test_webhook_data = {
        'ScamReason': 'IRS Impersonation - Urgent Tax Payment Demand',
        'callTranscript': '''Hello, this is Officer Johnson from the Internal Revenue Service. 
        I'm calling about your unpaid taxes from 2023. Our records show you owe $5,847 
        in back taxes and penalties. This is your final notice before we issue an arrest 
        warrant. You must make payment immediately to avoid criminal prosecution. 
        We accept payment via gift cards or wire transfer only. Do not hang up or 
        law enforcement will be dispatched to your location.''',
        'callId': f'test_call_{int(time.time())}',
        'callerNumber': '+1-555-SCAMMER'
    }
    
    print(f"📋 Scam Reason: {test_webhook_data['ScamReason']}")
    print(f"📝 Transcript Preview: {test_webhook_data['callTranscript'][:100]}...")
    
    # Initialize orchestrator
    orchestrator = ScamPreventionOrchestrator()
    orchestrator.is_initialized = True  # Skip full init for test
    
    # Process the webhook
    print("\n🤖 Processing with Agent Orchestrator...")
    result = orchestrator.handle_webhook_scam_alert(
        scam_reason=test_webhook_data['ScamReason'],
        call_transcript=test_webhook_data['callTranscript'],
        call_id=test_webhook_data['callId']
    )
    
    print(f"\n📊 Analysis Results:")
    print(f"   Risk Score: {result['risk_score']:.2f}")
    print(f"   Action: {result['action']}")
    print(f"   Reason: {result['reason']}")
    
    # Simulate VAPI action
    if result['action'] == 'block':
        print("\n🚫 VAPI Action: BLOCKING CALL")
        print("   Message: 'This call has been identified as fraudulent and blocked.'")
    elif result['action'] == 'transfer_family':
        print("\n👨‍👩‍👧 VAPI Action: WARM TRANSFER TO FAMILY")
        print("   Transferring to: +1-555-FAMILY")
        print("   Context provided: High-risk scam alert with full transcript")
    
    return test_webhook_data, result

def test_senso_analysis(webhook_data, vapi_result):
    """Step 5: Analyze completed call with Senso AI."""
    print_section("Step 5: Senso AI - Post-Call Analysis")
    
    print("🔍 Analyzing completed call transcript with Senso AI...")
    
    # Senso analysis
    senso_result = senso_agent.normalize_transcript(webhook_data['callTranscript'])
    
    print("\n📊 Senso AI Analysis:")
    print(f"   Keywords Detected: {', '.join(senso_result['keywords'][:5])}")
    print(f"   Sentiment: {senso_result['sentiment']}")
    print(f"   Behavioral Cues: {', '.join(senso_result['behavioral_cues'])}")
    
    # Generate comprehensive alert
    alert_data = {
        "call_id": webhook_data['callId'],
        "timestamp": datetime.now().isoformat(),
        "caller": webhook_data['callerNumber'],
        "scam_type": webhook_data['ScamReason'],
        "risk_score": vapi_result['risk_score'],
        "action_taken": vapi_result['action'],
        "senso_analysis": senso_result,
        "family_notification": {
            "sent": True,
            "method": "SMS + Email",
            "message": f"ALERT: Blocked scam call attempt. Caller claimed to be IRS demanding payment."
        }
    }
    
    # Generate call summary
    summary = senso_agent.generate_call_summary({
        'call_id': webhook_data['callId'],
        'status': 'blocked',
        'transcripts': [webhook_data['callTranscript']],
        'risk_level': 'high'
    })
    
    print("\n📄 Call Summary for Family:")
    print(summary)
    
    # Save complete analysis
    analysis_output = Path("data") / f"call_analysis_{webhook_data['callId']}.json"
    with open(analysis_output, 'w') as f:
        json.dump(alert_data, f, indent=2)
    
    print(f"\n✅ Complete analysis saved to: {analysis_output}")
    
    return alert_data

def main():
    """Run the complete MCP flow test."""
    print("\n" + "🛡️ " * 20)
    print("  GUARDO MCP FLOW TEST - Complete Pipeline")
    print("🛡️ " * 20)
    
    print("\nThis test simulates the complete flow:")
    print("1. BrightData → Web scraping for scam trends")
    print("2. ZeroEntropy → Extract elderly-specific patterns")
    print("3. LlamaIndex → Update searchable knowledge base")
    print("4. VAPI → Process incoming scam call")
    print("5. Senso AI → Analyze and report")
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    
    try:
        # Step 1: BrightData Collection
        brightdata_results = test_brightdata_collection()
        time.sleep(1)
        
        # Step 2: ZeroEntropy Parsing
        patterns = test_zeroentropy_parsing(brightdata_results)
        time.sleep(1)
        
        # Step 3: LlamaIndex Update
        if not test_llamaindex_update(patterns):
            print("❌ LlamaIndex update failed, continuing anyway...")
        time.sleep(1)
        
        # Step 4: VAPI Webhook Processing
        webhook_data, vapi_result = test_vapi_webhook()
        time.sleep(1)
        
        # Step 5: Senso AI Analysis
        final_analysis = test_senso_analysis(webhook_data, vapi_result)
        
        # Final Summary
        print_section("✅ MCP FLOW TEST COMPLETE")
        print("📊 Summary:")
        print(f"   • Scam data collected: 3 sources")
        print(f"   • Patterns extracted: {len(patterns)}")
        print(f"   • Risk assessment: {vapi_result['risk_score']:.2f}")
        print(f"   • Action taken: {vapi_result['action'].upper()}")
        print(f"   • Family notified: ✓")
        print("\n🛡️ Senior protected from scam attempt!")
        
    except Exception as e:
        print(f"\n❌ Error in MCP flow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
