"""
Vapi agent for call handling and warm transfers.
"""
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime

class VapiAgent:
    """Agent responsible for call handling, transcription, and transfers."""
    
    def __init__(self):
        self.active_calls = {}
        self.family_contacts = {
            "default": "+1-555-FAMILY"  # Demo number
        }
        self.senior_number = "+1-555-SENIOR"  # Demo number
        
    def answer_call(self, call_data: Dict[str, Any]) -> Dict[str, Any]:
        """Answer incoming call and start processing."""
        call_id = call_data.get("call_id", f"call_{int(time.time())}")
        
        # Store call in active calls
        self.active_calls[call_id] = {
            "call_id": call_id,
            "caller_number": call_data.get("from", "Unknown"),
            "start_time": datetime.now().isoformat(),
            "status": "answering",
            "transcripts": []
        }
        
        print(f"[Vapi] Answering call {call_id} from {call_data.get('from', 'Unknown')}")
        
        # Simulate answering with a greeting
        greeting = "Hello, you've reached the SafeSenior screening service. Please hold while we connect your call."
        
        return {
            "call_id": call_id,
            "status": "answered",
            "message": greeting,
            "action": "transcribe_initial"
        }
    
    def transcribe_call_segment(self, call_id: str, duration: int = 5) -> Dict[str, Any]:
        """Transcribe initial segment of the call for analysis."""
        if call_id not in self.active_calls:
            return {"error": "Call not found"}
        
        # Simulate transcription (in production, this would be real-time)
        # For demo, we'll use different test scenarios
        test_transcripts = [
            "This is the IRS calling about your unpaid taxes. You must pay immediately or face arrest.",
            "Hi grandma, it's me. I'm in trouble and need bail money. Please don't tell mom.",
            "Hello, this is your doctor's office calling to confirm your appointment tomorrow.",
            "You've won a million dollars! Just need your bank account to deposit the prize."
        ]
        
        # Use caller number to deterministically select a test transcript
        caller = self.active_calls[call_id].get("caller_number", "Unknown")
        transcript_index = hash(caller) % len(test_transcripts)
        transcript = test_transcripts[transcript_index]
        
        # Store transcript
        self.active_calls[call_id]["transcripts"].append({
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "text": transcript
        })
        
        print(f"[Vapi] Transcribed {duration}s: '{transcript[:50]}...'")
        
        return {
            "call_id": call_id,
            "transcript": transcript,
            "duration": duration,
            "status": "transcribed"
        }
    
    def warm_transfer(self, call_id: str, transfer_to: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a warm transfer with context handoff."""
        if call_id not in self.active_calls:
            return {"error": "Call not found"}
        
        call = self.active_calls[call_id]
        risk_level = context.get("risk_score", 0)
        
        if transfer_to == "family":
            # High risk - transfer to family member
            transfer_number = self.family_contacts["default"]
            
            # Prepare context for family member
            family_context = {
                "alert": "SCAM ALERT: High-risk call detected",
                "caller": call["caller_number"],
                "risk_score": risk_level,
                "matched_patterns": context.get("matched_patterns", []),
                "transcript_preview": call["transcripts"][0]["text"][:100] if call["transcripts"] else ""
            }
            
            # Simulate warm transfer
            print(f"[Vapi] WARM TRANSFER to FAMILY at {transfer_number}")
            print(f"[Vapi] Context: {json.dumps(family_context, indent=2)}")
            
            # Play message to caller
            caller_message = "One moment please, I'm transferring you to the authorized contact."
            
            # Update call status
            call["status"] = "transferred_to_family"
            call["transfer_reason"] = "high_risk_scam"
            
            return {
                "call_id": call_id,
                "action": "warm_transfer",
                "transfer_to": "family",
                "transfer_number": transfer_number,
                "context": family_context,
                "caller_message": caller_message
            }
            
        elif transfer_to == "senior":
            # Low risk - transfer to senior
            transfer_number = self.senior_number
            
            # Prepare friendly context
            senior_context = {
                "caller": call["caller_number"],
                "screening_result": "passed",
                "risk_level": "low"
            }
            
            print(f"[Vapi] Normal transfer to SENIOR at {transfer_number}")
            print(f"[Vapi] Call appears safe, transferring normally")
            
            # Update call status
            call["status"] = "transferred_to_senior"
            
            return {
                "call_id": call_id,
                "action": "normal_transfer",
                "transfer_to": "senior",
                "transfer_number": transfer_number,
                "context": senior_context
            }
        
        else:
            return {"error": "Invalid transfer target"}
    
    def block_call(self, call_id: str, reason: str) -> Dict[str, Any]:
        """Block a high-risk call."""
        if call_id not in self.active_calls:
            return {"error": "Call not found"}
        
        call = self.active_calls[call_id]
        
        # Play warning message
        warning_message = "This call has been identified as potentially fraudulent and has been blocked. If you believe this is an error, please contact our support."
        
        print(f"[Vapi] BLOCKING CALL {call_id} - Reason: {reason}")
        
        # Update call status
        call["status"] = "blocked"
        call["block_reason"] = reason
        
        # Log incident
        self._log_incident(call_id, "call_blocked", reason)
        
        return {
            "call_id": call_id,
            "action": "block",
            "message": warning_message,
            "reason": reason
        }
    
    def monitor_call(self, call_id: str) -> Dict[str, Any]:
        """Continue monitoring an ongoing call."""
        if call_id not in self.active_calls:
            return {"error": "Call not found"}
        
        # In production, this would set up continuous monitoring
        print(f"[Vapi] Monitoring call {call_id} for suspicious activity")
        
        return {
            "call_id": call_id,
            "status": "monitoring",
            "message": "Call monitoring active"
        }
    
    def _log_incident(self, call_id: str, incident_type: str, details: str):
        """Log security incidents for reporting."""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "call_id": call_id,
            "type": incident_type,
            "details": details
        }
        print(f"[Vapi] INCIDENT LOG: {json.dumps(incident)}")

# Create singleton instance
vapi_agent = VapiAgent()
