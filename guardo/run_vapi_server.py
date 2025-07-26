#!/usr/bin/env python3
"""
Main server script to run VAPI webhook with full agent integration.
Combines the webhook approach from vapiTesting.py with the agent architecture.
"""

import os
import sys
from pathlib import Path

# Add the guardo directory to Python path
sys.path.append(str(Path(__file__).parent))

from src.vapi_handler import vapi_webhook_server, vapi_agent
from src.agent_orchestrator import ScamPreventionOrchestrator

def main():
    print("🛡️  Guardo: AI-Powered Scam Protection for Seniors")
    print("=" * 60)
    
    # Initialize the agent orchestrator
    print("🔧 Initializing agent orchestrator...")
    orchestrator = ScamPreventionOrchestrator()
    
    # Set up the knowledge pipeline
    print("📚 Setting up knowledge pipeline...")
    if orchestrator.setup_knowledge_pipeline():
        print("✅ Knowledge pipeline initialized successfully!")
    else:
        print("❌ Failed to initialize knowledge pipeline")
        return
    
    # Integrate orchestrator with webhook server
    print("🔗 Integrating orchestrator with webhook server...")
    
    # Monkey patch the webhook server to use orchestrator
    original_process_scam_alert = vapi_webhook_server._process_scam_alert
    
    def enhanced_process_scam_alert(call_id: str, scam_reason: str, transcript: str):
        """Enhanced scam alert processing using orchestrator."""
        print(f"\n🚨 SCAM ALERT from VAPI webhook!")
        print(f"📞 Call ID: {call_id}")
        print(f"⚠️  Reason: {scam_reason}")
        print(f"📝 Transcript: {transcript[:100]}...")
        
        # Use orchestrator for enhanced processing
        orchestrator_result = orchestrator.handle_webhook_scam_alert(
            scam_reason=scam_reason,
            call_transcript=transcript,
            call_id=call_id
        )
        
        # Convert orchestrator decision to VAPI action
        action = orchestrator_result.get("action", "transfer_normal")
        context = orchestrator_result.get("context", {})
        
        if action == "block":
            return vapi_agent.block_call(call_id, orchestrator_result.get("reason", "Scam detected"))
        elif action == "transfer_family":
            return vapi_agent.warm_transfer(call_id, "family", context)
        elif action == "transfer_monitor":
            transfer_result = vapi_agent.warm_transfer(call_id, "senior", context)
            vapi_agent.monitor_call(call_id)
            return transfer_result
        else:
            return vapi_agent.warm_transfer(call_id, "senior", context)
    
    # Replace the webhook server's processing function
    vapi_webhook_server._process_scam_alert = enhanced_process_scam_alert
    
    print("🚀 Starting VAPI webhook server with full agent integration...")
    print("📡 Webhook endpoints will be available at:")
    print("   - POST /scamHandling  (main webhook)")
    print("   - GET  /health        (health check)")
    print("   - GET  /calls/{id}    (call info)")
    print()
    
    # Start the server
    try:
        vapi_webhook_server.run_server(port=8000, use_ngrok=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Guardo server...")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
