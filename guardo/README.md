# Guardo - AI Scam Protection for Seniors

Guardo is a multi-agent voice AI system that protects seniors from phone scams in real-time. It orchestrates multiple AI agents to provide comprehensive scam detection and prevention:

- **Vapi Agent**: Handles call answering, transcription, and warm transfers
- **LlamaIndex Agent**: Indexes and queries scam patterns for real-time detection
- **Senso.ai Agent**: Enhances transcript analysis with behavioral insights
- **ZeroEntropy Agent**: Interprets scam articles to extract elderly-specific patterns
- **BrightData (MCP)**: Simulated scam article data source

## Features

- **Real-time scam detection**: Analyze text for scam patterns and suspicious content
- **Vector-based similarity matching**: Uses advanced embeddings to detect scam variations
- **Configurable thresholds**: Adjust sensitivity based on your needs
- **Batch processing**: Analyze multiple texts at once
- **Extensible architecture**: Easy to add new data sources and detection methods

## Project Structure

```
guardo/
├── data/
│   ├── scam_phrases.json      # Manual scam phrases database
│   └── scam_articles.json     # Simulated BrightData articles via MCP
├── src/
│   ├── vapi_handler.py        # Vapi agent for call handling & warm transfers
│   ├── llama_index.py         # LlamaIndex agent for scam pattern matching
│   ├── senso_processor.py     # Senso.ai agent for transcript analysis
│   ├── zeroEntropy_parser.py  # ZeroEntropy agent for article interpretation
│   ├── agent_orchestrator.py  # Main orchestrator connecting all agents
│   └── config.py              # Configuration and API keys
├── main.py                    # Demo script showing agent cooperation
├── requirements.txt           # Dependencies: llama-index, vapi-sdk, requests
├── PRD.md                     # Product requirements document
└── README.md                  # This file
```

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/arassiq/SafeSenior.git
   cd SafeSenior/guardo
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export VAPI_API_KEY="your-vapi-key"           # For call handling
   export SENSO_AI_API_KEY="your-senso-key"      # For transcript analysis
   export ZEROENTROPY_API_KEY="your-ze-key"      # For document retrieval
   export BRIGHTDATA_API_KEY="your-bd-key"       # For scam data (optional)
   export OPENAI_API_KEY="your-openai-key"       # For embeddings (optional)
   ```

## Quick Start

1. **Run the demo**:
   ```bash
   python main.py
   ```

   This will:
   - Initialize all AI agents
   - Build the scam knowledge base
   - Simulate incoming calls
   - Demonstrate warm transfers for scam calls

2. **Using the orchestrator programmatically**:
   ```python
   from src.agent_orchestrator import ScamPreventionOrchestrator

   # Initialize the multi-agent system
   orchestrator = ScamPreventionOrchestrator()
   orchestrator.setup_knowledge_pipeline()

   # Handle an incoming call
   call_data = {
       "call_id": "call_123",
       "from": "+1-555-UNKNOWN",
       "to": "+1-555-SENIOR"
   }
   
   result = orchestrator.handle_incoming_call(call_data)
   print(f"Action taken: {result['action']}")
   ```

## Configuration

Edit `src/config.py` to customize:

- **SCAM_THRESHOLD**: Minimum score to classify as scam (0.0-1.0)
- **SIMILARITY_TOP_K**: Number of similar phrases to retrieve
- **Data paths**: Locations for data, indexes, and logs

## Adding New Scam Data

1. **Add phrases to data file**:
   ```bash
   echo "New suspicious phrase" >> data/scam_phrases.txt
   ```

2. **Rebuild the index**:
   ```bash
   python main.py
   ```

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## API Usage (Future Extension)

The system is designed to be easily extended with a REST API:

```python
from fastapi import FastAPI
from src.querying import ScamDetector

app = FastAPI()

@app.post("/detect")
async def detect_scam(text: str):
    result = detector.detect_scam(text)
    return result
```

## Integration with VAPI

For phone call integration:

1. **Set up webhook endpoint** to receive call transcripts
2. **Process audio in real-time** using the scam detector
3. **Trigger alerts** when scams are detected
4. **Implement warm transfers** to family members or authorities

## Performance Considerations

- **Index caching**: Indexes are saved to disk for faster startup
- **Batch processing**: Use `batch_detect()` for multiple texts
- **Memory usage**: Large datasets may require chunking
- **Response time**: Typical detection takes 50-200ms

## Logging

Logs are written to:
- **Console**: Real-time output
- **Files**: `logs/` directory with module-specific logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the SafeSenior initiative to protect elderly individuals from scams.

## Support

For issues and questions:
- Check the test files for usage examples
- Review the configuration options
- Examine the log files for debugging information

---

**Note**: This system is designed to assist in scam detection but should not be the only line of defense. Always encourage seniors to verify suspicious calls through official channels.
