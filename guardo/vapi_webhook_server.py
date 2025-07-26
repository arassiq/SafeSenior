from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/vapi/webhook', methods=['POST'])
def vapi_webhook():
    """Handle incoming Vapi webhooks"""
    data = request.get_json()
    
    print(f"[{datetime.now()}] Vapi webhook received:")
    print(json.dumps(data, indent=2))
    
    # Handle different event types
    event_type = data.get('message', {}).get('type')
    
    if event_type == 'transcript':
        # Handle transcript events
        transcript = data.get('message', {}).get('transcript')
        print(f"Transcript: {transcript}")
        
        # Here you would integrate with your Guardo agents
        # For now, just acknowledge
        return jsonify({"status": "received", "transcript_processed": True})
    
    elif event_type == 'function-call':
        # Handle function calls
        function_call = data.get('message', {}).get('functionCall')
        print(f"Function call: {function_call}")
        
        return jsonify({"result": "Function processed"})
    
    else:
        return jsonify({"status": "received"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Guardo Vapi Webhook"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting Guardo Vapi webhook server on port {port}")
    print(f"Vapi API Key configured: {'Yes' if os.getenv('VAPI_API_KEY') else 'No'}")
    app.run(host='0.0.0.0', port=port, debug=True)
