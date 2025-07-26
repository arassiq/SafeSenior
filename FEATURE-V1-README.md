# Guardo Feature-V1 Branch

## Overview
The `feature-v1` branch successfully combines the comprehensive agent architecture from `feature-warm-transfers` with the VAPI webhook integration from `vapiTesting`. This creates a unified system for AI-powered scam protection for seniors.

## What's Included

### 🤖 Agent Architecture (from feature-warm-transfers)
- **LlamaIndex Agent**: Scam pattern detection with local HuggingFace embeddings
- **ZeroEntropy Agent**: Document parsing and elderly-specific pattern extraction  
- **Senso Agent**: Transcript normalization and behavioral analysis
- **Agent Orchestrator**: Coordinates all agents for comprehensive scam detection

### 📞 VAPI Integration (from vapiTesting)
- **Webhook Server**: FastAPI server to receive VAPI scam alerts
- **Ngrok Integration**: Public URL exposure for webhook endpoints
- **Real-time Processing**: Immediate scam alert handling from VAPI

### 🧠 Enhanced Features
- **Risk Assessment**: Combined risk scoring from multiple AI agents
- **Warm Transfers**: Context-aware call routing (senior vs family)
- **Call Blocking**: Automatic blocking of high-risk scam calls
- **Monitoring**: Continuous call monitoring for medium-risk calls

## Quick Start

### 1. Install Dependencies
```bash
cd guardo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install llama-index-embeddings-huggingface  # For local embeddings
```

### 2. Set Up Environment
Create a `.env` file:
```env
BRIGHTDATA_API_KEY=your_brightdata_key
ZEROENTROPY_API_KEY=your_zeroentropy_key  
SENSO_API_KEY=your_senso_key
VAPI_API_KEY=your_vapi_key
```

### 3. Test Components (Non-VAPI)
```bash
python test_components.py
```

### 4. Run Full VAPI Server
```bash
python run_vapi_server.py
```
This will:
- Initialize all AI agents
- Set up the knowledge pipeline
- Start the webhook server with ngrok
- Display public webhook URL for VAPI configuration

## Architecture Flow

### Knowledge Pipeline
1. **ZeroEntropy** parses scam articles and extracts elderly-specific patterns
2. **LlamaIndex** indexes all scam patterns for fast similarity search
3. **Agent Orchestrator** coordinates the knowledge building process

### Real-time Call Processing
1. **VAPI** sends webhook alert with scam reason and transcript
2. **Webhook Server** receives and processes the alert
3. **Agent Orchestrator** analyzes using all agents:
   - LlamaIndex pattern matching
   - Senso transcript enhancement  
   - Combined risk assessment
4. **Decision Engine** determines action:
   - Block call (high risk)
   - Transfer to family (high risk)
   - Transfer with monitoring (medium risk)
   - Normal transfer (low risk)

## Key Files

### Core Agent Files
- `src/agent_orchestrator.py` - Main orchestration logic
- `src/llama_index.py` - Scam pattern detection
- `src/zeroEntropy_parser.py` - Document parsing
- `src/senso_processor.py` - Transcript analysis
- `src/vapi_handler.py` - VAPI webhook server

### Entry Points
- `run_vapi_server.py` - Main server for production
- `test_components.py` - Component testing
- `vapiTesting.py` - Original VAPI testing script

### Data Files
- `data/scam_phrases.json` - Known scam phrases
- `data/scam_articles.json` - Processed scam articles
- `data/newsStories.json` - News stories for context

## Demo Capabilities

### Risk Detection
✅ IRS impersonation scams  
✅ Prize/lottery scams  
✅ Grandparent scams  
✅ Medicare/insurance scams  
✅ Warranty scams  
✅ Authority impersonation  

### Response Actions  
✅ Call blocking with warning message  
✅ Warm transfer to family with context  
✅ Normal transfer to senior  
✅ Continuous call monitoring  
✅ Incident logging and reporting  

## Testing

The system includes comprehensive tests for all components:
- **LlamaIndex**: Pattern matching with local embeddings
- **ZeroEntropy**: Elderly-specific pattern extraction  
- **BrightData**: Simulated data integration
- **Agent Orchestrator**: End-to-end workflow

All tests pass and demonstrate proper risk scoring and decision making.

## Production Readiness

This branch is ready for:
- ✅ Hackathon demonstration
- ✅ VAPI webhook integration  
- ✅ Real-time scam detection
- ✅ Multi-agent AI processing
- ⚠️  BrightData integration (simulated for demo)
- ⚠️  Senso integration (simulated for demo)

## Next Steps

1. **Real API Integration**: Replace simulated data with actual BrightData/Senso APIs
2. **Database Storage**: Add persistent storage for call logs and patterns
3. **Dashboard**: Create monitoring dashboard for family members
4. **Mobile App**: Develop companion mobile app for alerts
5. **Scaling**: Add Redis/database for multi-instance deployment

---

🛡️ **Guardo Feature-V1**: Protecting seniors with AI-powered scam detection!
