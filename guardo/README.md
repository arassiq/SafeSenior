# Guardo - Scam Detection System

Guardo is a scam detection system designed to protect senior citizens from phone and text scams using AI-powered analysis with LlamaIndex.

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
│   └── scam_phrases.txt   # Sample scam data
├── src/
│   ├── ingestion.py       # Data loading logic
│   ├── indexing.py        # Index creation with LlamaIndex
│   ├── querying.py        # Scam detection queries
│   ├── config.py          # Configuration settings
│   └── utils.py           # Helper functions
├── tests/
│   ├── test_ingestion.py  # Tests for data loading
│   ├── test_indexing.py   # Tests for index creation
│   └── test_querying.py   # Tests for querying
├── main.py                # Main script
├── requirements.txt       # Python dependencies
└── README.md              # This file
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

4. **Set up environment variables** (optional):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"  # If using OpenAI embeddings
   export ENVIRONMENT="development"  # or "production"
   ```

## Quick Start

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **Example usage in code**:
   ```python
   from src.config import get_config
   from src.ingestion import DataIngestion
   from src.indexing import ScamIndexer
   from src.querying import ScamDetector

   # Initialize system
   config = get_config()
   ingestion = DataIngestion(config)
   data = ingestion.load_all_data()

   # Build index
   indexer = ScamIndexer(config)
   index = indexer.build_index(data)

   # Detect scams
   detector = ScamDetector(config, index)
   result = detector.detect_scam("You've won a $1000 prize! Call now!")
   
   print(f"Is scam: {result['is_scam']}")
   print(f"Risk score: {result['risk_score']}")
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
