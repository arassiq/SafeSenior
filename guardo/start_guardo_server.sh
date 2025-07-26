#!/bin/bash

echo "🛡️  Starting Guardo SafeSenior System"
echo "====================================="

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded"
else
    echo "⚠️  Warning: .env file not found"
fi

# Start ngrok in background
echo "🌐 Starting ngrok tunnel..."
ngrok http 8080 --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!
echo "✓ ngrok started (PID: $NGROK_PID)"

# Wait for ngrok to initialize
sleep 3

# Get the public URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null)

if [ ! -z "$NGROK_URL" ]; then
    echo "✓ ngrok tunnel active: $NGROK_URL"
    echo "📋 Webhook URL: $NGROK_URL/vapi/webhook"
else
    echo "⚠️  Could not retrieve ngrok URL"
fi

# Start the Vapi webhook server
echo "🚀 Starting Vapi webhook server..."
python3 vapi_webhook_server.py

# Cleanup on exit
trap "kill $NGROK_PID 2>/dev/null" EXIT
