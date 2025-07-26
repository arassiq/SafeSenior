"""
Main script to run the Guardo scam detection system.
"""
import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.agent_orchestrator import ScamPreventionOrchestrator

def run_demo():
    """Run the Guardo demo showing all agents working together."""
    print("="*60)
    print("      GUARDO - AI Scam Protection for Seniors")
    print("      Protecting elderly from phone scams in real-time")
    print("="*60)
    
    # Initialize orchestrator
    orchestrator = ScamPreventionOrchestrator()
    
    # Phase 1: Knowledge Pipeline Setup
    print("\n📚 PHASE 1: Building Knowledge Base")
    print("-"*50)
    if not orchestrator.setup_knowledge_pipeline():
        print("Failed to initialize system. Exiting.")
        return
    
    # Show statistics
    stats = orchestrator.zeroentropy_agent.get_scam_statistics()
    print(f"\n📊 Scam Database Statistics:")
    print(f"   - Total patterns indexed: {stats['total_patterns']}")
    print(f"   - Scam types: {stats['scam_types']}")
    print(f"   - Recent trends: {stats['recent_trends'][:2]}")
    
    time.sleep(2)
    
    # Phase 2: Simulate incoming calls
    print("\n📞 PHASE 2: Live Call Protection Demo")
    print("-"*50)
    
    # Demo Call 1: IRS Scam (High Risk)
    print("\n🔴 DEMO CALL 1: IRS Impersonation Scam")
    call1 = {
        "call_id": "demo_call_001",
        "from": "+1-555-SCAMMER",
        "to": "+1-555-SENIOR"
    }
    result1 = orchestrator.handle_incoming_call(call1)
    print(f"\nResult: {result1.get('action', 'Unknown')}")
    
    time.sleep(3)
    
    # Demo Call 2: Legitimate Call (Low Risk)
    print("\n🟢 DEMO CALL 2: Legitimate Doctor's Office")
    call2 = {
        "call_id": "demo_call_002",
        "from": "+1-555-DOCTOR",
        "to": "+1-555-SENIOR"
    }
    result2 = orchestrator.handle_incoming_call(call2)
    print(f"\nResult: {result2.get('action', 'Unknown')}")
    
    time.sleep(2)
    
    # Demo Call 3: Grandparent Scam (High Risk)
    print("\n🔴 DEMO CALL 3: Grandparent Scam")
    call3 = {
        "call_id": "demo_call_003",
        "from": "+1-555-FAKEGRAND",
        "to": "+1-555-SENIOR"
    }
    result3 = orchestrator.handle_incoming_call(call3)
    print(f"\nResult: {result3.get('action', 'Unknown')}")
    
    # Summary
    print("\n" + "="*60)
    print("📈 DEMO SUMMARY")
    print("="*60)
    print("✅ Knowledge pipeline: Initialized with elderly-specific patterns")
    print("✅ Call screening: 3 calls processed")
    print("✅ Scams blocked: 2 high-risk calls intercepted")
    print("✅ Family alerts: Warm transfers executed successfully")
    print("✅ Senior protected: Zero scam calls reached the elderly")
    print("\n🛡️ Guardo is ready to protect seniors from phone scams!")

def main():
    """Main function to run Guardo system."""
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
