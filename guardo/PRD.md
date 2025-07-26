PRD for Guardo: Scam Detection for Seniors1. What is Guardo?Guardo is a voice AI system to protect seniors from phone scams. It uses Vapi for call handling, LlamaIndex for scam detection, Senso.ai for transcript analysis, BrightData for scam data, and ZeroEntropy for data interpretation. Calls route through a Vapi number, with an AI agent screening for scams, transferring safe calls to seniors, and escalating high-risk calls to family via warm transfers. Conference calls are avoided due to transcription issues.2. GoalsDetect phone scams in real-time.
Protect seniors with simple voice interactions.
Alert family for high-risk calls.
Build a 3-minute demo. 

3. FeaturesLayer 1: Pre-fingerprinting (Simulated):BrightData: Scrapes North American scam articles via MCP (simulated with JSON).
ZeroEntropy: Interprets articles for elderly-specific scams (e.g., grandparent scams).
LlamaIndex: Indexes scam data for querying.

Layer 2: Call Pre-screening (Core):Vapi: Answers calls, transcribes first 5 seconds, checks for scams (e.g., “FBI”).
Senso.ai: Normalizes transcripts into JSON.
LlamaIndex: Queries scam index to detect risks.
Action: Warns, blocks, or warm-transfers to senior.

Layer 3: Monitoring & Intervention (Simulated):Vapi + Senso.ai: Monitors calls, updates transcript data.
LlamaIndex: Re-queries for ongoing risks.
Action: Warns senior, warm-transfers to family, logs alert (print statement).

4. How It WorksZeroEntropy pulls scam articles via BrightData’s MCP (simulated JSON).
LlamaIndex indexes data for fast scam detection.
Vapi answers call, sends transcript to Senso.ai for normalization.
LlamaIndex queries index to detect scams.
Vapi acts: warns, transfers, or escalates.
Log results for demo.

5. IntegrationsVapi: Call answering, transcription, warm transfers (Layers 2 & 3).
LlamaIndex: Indexes and queries scam data (Layers 1 & 2). Built-in query engine and vector store enable fast, context-aware scam detection.
Senso.ai: Normalizes transcripts via MCP (Layers 2 & 3).
BrightData: Provides scam articles via MCP (Layer 1, simulated).
ZeroEntropy: Interprets BrightData data for elderly scams (Layer 1).
MCP: Enables agent communication (simulated as JSON).
Other Providers: Skip Datadog/Mixpanel MCP to focus on core tools.

6. Python vs. TypeScriptPython: Used for LlamaIndex, Senso.ai, ZeroEntropy, and BrightData due to native support and AI compatibility.
TypeScript: Not used; Python is faster for hackathon.
Decision: Stick with Python for demo.

7. SecurityEncrypt transcripts (AES-256).
Use HTTPS for APIs.
Plan for HIPAA/GDPR (not in demo).

8. Demo (3 Minutes)0:00–0:30: Introduce Guardo’s mission.
0:30–1:30: Show Vapi flagging a scam call (e.g., “IRS owes you”).
1:30–2:30: Display LlamaIndex query results, Senso.ai JSON, ZeroEntropy data.
2:30–3:00: Show Vapi warning and simulated family alert.

9. Repo Structure

guardo/
├── data/
│   └── scam_articles.json  # Simulated BrightData data
                 scam_phrases.json # Manully inputted scam phrases
	
├── src/
│   ├── vapi_handler.py     # Vapi call handling
│   ├── llama_index.py      # LlamaIndex indexing/querying
│   ├── senso_processor.py  # Senso.ai normalization
│   ├── zeroEntropy_parser.py       # ZeroEntropy data parsing
│   └── config.py          # API keys, paths
├── main.py                # Main script
├── requirements.txt       # Deps: llama-index, vapi-sdk, requests
└── README.md              # Setup guide

10. SetupInstall: pip install llama-index vapi-sdk requests.
Add scam_articles.json to data/.
Get API keys from Vapi, Senso.ai, ZeroEntropy, BrightData.
Run python main.py.

11. LLM NotesFocus on Layer 2 (Vapi + LlamaIndex).
Simulate Layer 1 with JSON (ZeroEntropy + BrightData).
Mock Layer 3 alerts with prints.
Use MCP as JSON exchanges.
Keep Python code simple for 4-hour hackathon.

