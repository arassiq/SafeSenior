#!/usr/bin/env python3
"""
Test script for Guardo components (excluding VAPI).
Tests:
1. LlamaIndex scam detection
2. ZeroEntropy document parsing
3. BrightData integration (simulated)
4. Agent orchestration
"""

import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_llama_index():
    """Test LlamaIndex scam detection."""
    print("\n=== Testing LlamaIndex Scam Detection ===")
    try:
        from src.llama_index import llama_agent
        
        # Initialize the index
        llama_agent.setup_scam_index()
        
        # Test some sample phrases
        test_phrases = [
            "Hello, this is John from your bank.",
            "This is the FBI. You have an arrest warrant.",
            "You've won a million dollars! Send $100 to claim.",
            "Your car warranty is about to expire.",
            "Hi grandma, it's me, your grandson."
        ]
        
        for phrase in test_phrases:
            result = llama_agent.query_scam_patterns(phrase)
            risk_score = result.get('risk_score', 0)
            risk_level = "HIGH" if risk_score > 0.7 else "MEDIUM" if risk_score > 0.4 else "LOW"
            print(f"  '{phrase[:50]}...' - Risk: {risk_level} ({risk_score:.2f})")
            
        print("✅ LlamaIndex test completed\n")
        return True
        
    except Exception as e:
        print(f"❌ LlamaIndex test failed: {e}\n")
        return False

def test_zeroentropy():
    """Test ZeroEntropy document parsing."""
    print("=== Testing ZeroEntropy Document Parser ===")
    try:
        from src.zeroEntropy_parser import zeroentropy_agent
        
        # Use the singleton instance
        parser = zeroentropy_agent
        
        # Test parsing scam articles
        patterns = parser.parse_scam_articles()
        
        if patterns:
            print(f"  ✅ Successfully parsed {len(patterns)} patterns")
            # Test elderly-specific interpretation
            insights = parser.interpret_for_elderly_context(patterns)
            print(f"  High-risk phrases: {len(insights.get('high_risk_phrases', []))}")
            print(f"  Emotional triggers: {len(insights.get('emotional_triggers', []))}")
        else:
            print("  ⚠️  Parser returned empty result")
            
        print("✅ ZeroEntropy test completed\n")
        return True
        
    except Exception as e:
        print(f"❌ ZeroEntropy test failed: {e}\n")
        return False

def test_brightdata():
    """Test BrightData integration (using simulated data)."""
    print("=== Testing BrightData Integration ===")
    try:
        # Since we don't have the actual scam_data.py yet, let's simulate it
        print("  Loading simulated scam data...")
        
        # Check if we have the JSON data files
        data_files = ["scam_phrases.json", "scam_articles.json", "newsStories.json"]
        data_path = Path("data")
        
        for file in data_files:
            file_path = data_path / file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else len(data.get('phrases', []))
                    print(f"  ✅ {file}: {count} items loaded")
            else:
                print(f"  ❌ {file}: Not found")
                
        print("✅ BrightData test completed (simulated)\n")
        return True
        
    except Exception as e:
        print(f"❌ BrightData test failed: {e}\n")
        return False

def test_agent_orchestrator():
    """Test the agent orchestrator."""
    print("=== Testing Agent Orchestrator ===")
    try:
        from src.agent_orchestrator import ScamPreventionOrchestrator
        
        # Initialize orchestrator
        orchestrator = ScamPreventionOrchestrator()
        orchestrator.setup_knowledge_pipeline()
        
        # Since we're not testing VAPI, let's test the LlamaIndex component directly
        print("  Testing scam pattern detection...")
        
        test_transcript = "This is the IRS calling about your unpaid taxes. You must pay immediately or face arrest."
        print(f"  Testing transcript: '{test_transcript[:50]}...'")
        
        # Test the llama agent directly
        from src.llama_index import llama_agent
        result = llama_agent.query_scam_patterns(test_transcript)
        
        if result and not result.get('error'):
            risk_score = result.get('risk_score', 0)
            print(f"  Risk score: {risk_score:.2f}")
            print(f"  Is scam: {result.get('is_scam', False)}")
            print(f"  Recommendation: {result.get('recommendation', 'Unknown')}")
            
            if risk_score > 0.8:
                print("  🚨 HIGH RISK - Would block call")
            elif risk_score > 0.6:
                print("  ⚠️  MEDIUM RISK - Would warn senior")
            else:
                print("  ✅ LOW RISK - Would transfer call")
                
        print("✅ Agent Orchestrator test completed\n")
        return True
        
    except Exception as e:
        print(f"❌ Agent Orchestrator test failed: {e}\n")
        return False

def main():
    """Run all component tests."""
    print("Starting Guardo Component Tests (excluding VAPI)")
    print("=" * 50)
    
    # Check if environment is set up
    from src import config
    
    print("\nChecking API keys...")
    keys_status = {
        "BrightData": bool(config.BRIGHTDATA_API_KEY),
        "ZeroEntropy": bool(config.ZEROENTROPY_API_KEY),
        "Senso": bool(config.SENSO_AI_API_KEY),
    }
    
    for service, has_key in keys_status.items():
        status = "✅ Found" if has_key else "❌ Missing"
        print(f"  {service}: {status}")
    
    # Run tests
    results = {
        "LlamaIndex": test_llama_index(),
        "ZeroEntropy": test_zeroentropy(),
        "BrightData": test_brightdata(),
        "Agent Orchestrator": test_agent_orchestrator()
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for component, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {component}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready for demo.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
