"""
Vapi agent for call handling and warm transfers.
"""
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
from .zeroEntropy_parser import zeroentropy_agent

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

    def get_call_summary(self, call_id: str) -> Dict[str, Any]:
        """Get summary of call for reporting."""
        if call_id not in self.active_calls:
            return {"error": "Call not found"}
        
        call = self.active_calls[call_id]
        
        return {
            "call_id": call_id,
            "caller_number": call["caller_number"],
            "start_time": call["start_time"],
            "status": call["status"],
            "transcript_count": len(call["transcripts"]),
            "transcripts": call["transcripts"]
        }


class VapiWebhookServer:
    """FastAPI webhook server for VAPI integration."""
    
    def __init__(self, vapi_agent: VapiAgent):
        self.app = FastAPI()
        self.vapi_agent = vapi_agent
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Set up routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up FastAPI routes."""
        
        @self.app.post("/scamHandling")
        async def scam_handling(request: Request):
            """Handle scam detection webhook from VAPI."""
            try:
                data = await request.json()
                scam_reason = data.get('ScamReason', '')
                call_transcript = data.get('callTranscript', '')
                call_id = data.get('callId', f"webhook_{int(time.time())}")
                
                print(f"[VAPI Webhook] Received scam alert: {scam_reason}")
                print(f"[VAPI Webhook] Transcript: {call_transcript[:100]}...")
                
                # Create call data if not exists
                if call_id not in self.vapi_agent.active_calls:
                    call_data = {
                        "call_id": call_id,
                        "from": data.get('callerNumber', 'Unknown')
                    }
                    self.vapi_agent.answer_call(call_data)
                
                # Process the scam alert
                result = self._process_scam_alert(call_id, scam_reason, call_transcript)
                
                return {"status": "ok", "result": result}
                
            except Exception as e:
                print(f"[VAPI Webhook] Error processing request: {e}")
                return {"status": "error", "message": str(e)}
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "Guardo VAPI Webhook"}
        
        @self.app.get("/calls/{call_id}")
        async def get_call_info(call_id: str):
            """Get information about a specific call."""
            return self.vapi_agent.get_call_summary(call_id)
    
    def _process_scam_alert(self, call_id: str, scam_reason: str, transcript: str) -> Dict[str, Any]:
        """Process a scam alert using ZeroEntropy analysis exclusively."""
        print(f"[VAPI] Processing scam alert with ZeroEntropy analysis (VAPI reason: {scam_reason})")
        
        # Use ZeroEntropy exclusively for analysis
        zeroentropy_analysis = zeroentropy_agent.analyze_transcript_for_scam(transcript)
        
        # Use ZeroEntropy risk score as the primary score
        risk_score = zeroentropy_analysis.get("risk_score", 0.0)
        
        context = {
            "risk_score": risk_score,
            "vapi_scam_reason": scam_reason,  # Keep VAPI reason for context
            "transcript": transcript,
            "zeroentropy_analysis": zeroentropy_analysis,
            "matched_patterns": zeroentropy_analysis.get("matched_patterns", []),
            "scam_indicators": zeroentropy_analysis.get("scam_indicators", [])
        }
        
        print(f"[VAPI] ZeroEntropy risk assessment: {risk_score:.2f} ({zeroentropy_analysis.get('confidence', 'unknown')} confidence)")
        
        if risk_score > 0.8:
            # High risk - block or transfer to family based on ZeroEntropy analysis
            if any(indicator in context["scam_indicators"] for indicator in ["irs", "arrest", "warrant", "fbi"]):
                return self.vapi_agent.block_call(call_id, f"ZeroEntropy high-risk detection: {risk_score:.2f}")
            else:
                return self.vapi_agent.warm_transfer(call_id, "family", context)
        elif risk_score > 0.5:
            # Medium risk - transfer with monitoring
            transfer_result = self.vapi_agent.warm_transfer(call_id, "senior", context)
            self.vapi_agent.monitor_call(call_id)
            return transfer_result
        else:
            # Low risk - normal transfer
            return self.vapi_agent.warm_transfer(call_id, "senior", context)
    
    def _assess_risk_from_reason(self, scam_reason: str) -> float:
        """Assess risk score from scam reason."""
        reason_lower = scam_reason.lower()
        
        # High risk patterns
        if any(keyword in reason_lower for keyword in ["irs", "fbi", "arrest", "warrant", "police"]):
            return 0.9
        elif any(keyword in reason_lower for keyword in ["urgent", "immediate", "emergency"]):
            return 0.8
        elif any(keyword in reason_lower for keyword in ["prize", "won", "lottery", "winner"]):
            return 0.75
        elif any(keyword in reason_lower for keyword in ["medicare", "insurance", "social security"]):
            return 0.7
        else:
            return 0.6
    
    def run_server(self, port: int = 8000, use_ngrok: bool = True):
        """Run the webhook server."""
        if use_ngrok:
            try:
                public_url = ngrok.connect(port).public_url
                print(f"🌐 Public ngrok URL: {public_url}")
                print(f"📞 Scam Endpoint: {public_url}/scamHandling")
                print(f"❤️  Health Check: {public_url}/health")
            except Exception as e:
                print(f"⚠️  Ngrok failed: {e}. Running locally only.")
        
        print(f"🚀 Starting VAPI webhook server on port {port}...")
        uvicorn.run(self.app, host="0.0.0.0", port=port)


# Create singleton instances
vapi_agent = VapiAgent()
vapi_webhook_server = VapiWebhookServer(vapi_agent)


# Convenience function to start the server
def start_vapi_server(port: int = 8000, use_ngrok: bool = True):
    """Start the VAPI webhook server."""
    vapi_webhook_server.run_server(port=port, use_ngrok=use_ngrok)
