#!/usr/bin/env python3
"""
Test script to verify ZeroEntropy API integration
"""
import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from zeroEntropy_parser import zeroentropy_agent

def test_zeroentropy_integration():
    """Test ZeroEntropy API integration"""
    print("🧪 Testing ZeroEntropy Integration (API Mode)")
    print("=" * 50)
    
    # Test sample transcripts
    test_transcripts = [
        "This is the IRS calling about your unpaid taxes. You must pay immediately or face arrest.",
        "Hi grandma, it's me. I'm in trouble and need bail money. Please don't tell mom.",
        "Hello, this is your doctor's office calling to confirm your appointment tomorrow.",
        "You've won a million dollars! Just need your bank account to deposit the prize.",
        "This is Medicare calling about your benefits. We need to verify your social security number."
    ]
    
    for i, transcript in enumerate(test_transcripts, 1):
        print(f"\n📞 Test {i}: {transcript[:50]}...")
        
        # Analyze with ZeroEntropy
        result = zeroentropy_agent.analyze_transcript_for_scam(transcript)
        
        print(f"   Risk Score: {result['risk_score']:.2f}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Source: {result['analysis_source']}")
        print(f"   Matched Patterns: {len(result['matched_patterns'])}")
        if result['matched_patterns']:
            for pattern in result['matched_patterns']:
                print(f"     - {pattern}")
    
    print("\n✅ ZeroEntropy integration test completed!")
    print("\n🔑 API Status:")
    status = zeroentropy_agent.get_api_status()
    print(f"   Status: {status['status']}")
    print(f"   API Key: {status['api_key']}")
    if status['status'] == 'connected':
        print(f"   Total Snippets: {status['total_snippets']}")
    else:
        print(f"   Error: {status.get('error', 'Unknown')}")
    
    # Test API pattern fetch
    print("\n🔍 Testing pattern fetch...")
    patterns = zeroentropy_agent.fetch_scam_patterns()
    if patterns:
        print(f"   Fetched {len(patterns.get('snippets', []))} patterns")
        if 'snippets' in patterns:
            for snippet in patterns['snippets'][:3]:  # Show first 3
                print(f"     - {snippet.get('title', 'No title')}: {snippet.get('text', 'No text')[:50]}...")
    else:
        print("   Using fallback patterns")

if __name__ == "__main__":
    test_zeroentropy_integration()
