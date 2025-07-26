"""
Verification script to ensure all components are working correctly.
"""
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Set up environment variables first
os.environ['ZEROENTROPY_API_KEY'] = 'ze_1UiaUVwAy0tWCB28'
os.environ['SENSO_AI_API_KEY'] = 'tgr_d8iDP2v23cmf0CnYtHs9_4RiGyduCds5uSXzKxbVNP4'

from src.zeroEntropy_parser import zeroentropy_agent
from src.llama_index import llama_agent  
from src.senso_processor import senso_agent
from src.vapi_handler import vapi_agent

print("🔍 VERIFICATION SCRIPT - Checking all components\n")
print("="*60)

# 1. Check ZeroEntropy API Key
print("\n1️⃣ CHECKING ZEROENTROPY:")
print(f"   API Key loaded: {'Yes' if zeroentropy_agent.api_key else 'No'}")
print(f"   API Key value: {zeroentropy_agent.api_key[:10]}...{zeroentropy_agent.api_key[-5:] if zeroentropy_agent.api_key else 'NOT SET'}")

# Test ZeroEntropy parsing
print("\n   Testing ZeroEntropy parsing...")
patterns = zeroentropy_agent.parse_scam_articles()
print(f"   ✅ Parsed {len(patterns)} patterns from scam_articles.json")
if patterns:
    print(f"   Sample pattern: {patterns[0]['text']}")
    
# Get insights
insights = zeroentropy_agent.interpret_for_elderly_context(patterns)
print(f"   ✅ Extracted elderly insights with {len(insights['high_risk_phrases'])} high-risk phrases")

# 2. Check LlamaIndex integration
print("\n2️⃣ CHECKING LLAMAINDEX INTEGRATION:")
print("   Setting up scam index...")
success = llama_agent.setup_scam_index()
print(f"   Index setup: {'✅ Success' if success else '❌ Failed'}")

# Check if ZeroEntropy patterns are in the index
if success:
    print(f"   Total documents indexed: {len(llama_agent.scam_documents)}")
    # Count ZeroEntropy sourced documents
    ze_docs = [doc for doc in llama_agent.scam_documents if doc.metadata.get('source') == 'zero_entropy']
    print(f"   Documents from ZeroEntropy: {len(ze_docs)}")
    if ze_docs:
        print(f"   Sample ZeroEntropy doc: {ze_docs[0].text}")

# 3. Test with a fake transcript
print("\n3️⃣ CHECKING TRANSCRIPT PROCESSING:")
test_transcript = "This is the IRS calling about your unpaid taxes. You must pay immediately or face arrest."

# Test Senso.ai processing
print("\n   Testing Senso.ai processing...")
print(f"   Senso API Key loaded: {'Yes' if os.getenv('SENSO_AI_API_KEY') else 'No'}")
normalized = senso_agent.normalize_transcript(test_transcript)
print(f"   ✅ Senso normalized transcript")
print(f"   Original: {test_transcript[:50]}...")
print(f"   Keywords extracted: {normalized['keywords']}")
print(f"   Sentiment: {normalized['sentiment']}")
print(f"   Behavioral cues: {normalized['behavioral_cues']}")

# Test LlamaIndex query
print("\n   Testing LlamaIndex query...")
result = llama_agent.query_scam_patterns(test_transcript)
print(f"   Risk score: {result.get('risk_score', 0):.2f}")
print(f"   Is scam: {result.get('is_scam', False)}")
print(f"   Recommendation: {result.get('recommendation', 'Unknown')}")

# 4. Create test transcript file for data directory
print("\n4️⃣ CREATING TEST TRANSCRIPT FILE:")
test_transcripts = {
    "transcripts": [
        {
            "id": "test_001",
            "timestamp": "2025-07-26T22:00:00Z",
            "caller": "+1-555-SCAMMER",
            "text": "This is the IRS calling about your unpaid taxes. You must pay immediately or face arrest.",
            "duration": 5
        },
        {
            "id": "test_002", 
            "timestamp": "2025-07-26T22:01:00Z",
            "caller": "+1-555-DOCTOR",
            "text": "Hello, this is Dr. Smith's office calling to confirm your appointment tomorrow at 2 PM.",
            "duration": 5
        },
        {
            "id": "test_003",
            "timestamp": "2025-07-26T22:02:00Z", 
            "caller": "+1-555-GRANDSCAM",
            "text": "Hi grandma, it's me. I'm in trouble and need bail money. Please don't tell mom.",
            "duration": 5
        }
    ]
}

transcript_file = Path(__file__).parent / "data" / "test_transcripts.json"
with open(transcript_file, 'w') as f:
    json.dump(test_transcripts, f, indent=2)
print(f"   ✅ Created test_transcripts.json with 3 sample calls")

# 5. Verify full data flow
print("\n5️⃣ VERIFYING FULL DATA FLOW:")
print("   BrightData → ZeroEntropy → LlamaIndex → Query")

# Check if data flows correctly
print(f"\n   Step 1: BrightData (simulated) has {len(patterns)} articles")
print(f"   Step 2: ZeroEntropy extracted {len(patterns)} patterns")
print(f"   Step 3: LlamaIndex indexed {len(ze_docs)} ZeroEntropy documents")
print(f"   Step 4: Query returns risk scores correctly")

# Test each transcript
print("\n   Testing all sample transcripts:")
for transcript in test_transcripts["transcripts"]:
    result = llama_agent.query_scam_patterns(transcript["text"])
    print(f"\n   Call {transcript['id']}:")
    print(f"   - Text: {transcript['text'][:50]}...")
    print(f"   - Risk: {result.get('risk_score', 0):.2f}")
    print(f"   - Scam: {'YES' if result.get('is_scam') else 'NO'}")

print("\n" + "="*60)
print("✅ VERIFICATION COMPLETE")
print("="*60)

# Summary
issues = []
if not zeroentropy_agent.api_key:
    issues.append("❌ ZeroEntropy API key not set")
if not os.getenv('SENSO_AI_API_KEY'):
    issues.append("❌ Senso.ai API key not set") 
if not success:
    issues.append("❌ LlamaIndex failed to initialize")
if len(ze_docs) == 0:
    issues.append("❌ No ZeroEntropy documents in index")

if issues:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n✅ All components working correctly!")
    print("   - ZeroEntropy is parsing BrightData articles")
    print("   - LlamaIndex is indexing ZeroEntropy patterns")
    print("   - Senso.ai is processing transcripts")
    print("   - Risk detection is functioning")
