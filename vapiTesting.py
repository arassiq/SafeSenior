from vapi import Vapi
from fastapi import FastAPI, Request, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import uvicorn
import os


from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scamHandling")
async def scamHandling(request: Request):
    
    data = await request.json()

    print(data['ScamReason'], data['callTranscript'])

    return {"status": "ok"}


def run():
    port = 8000
    public_url = ngrok.connect(port).public_url
    print(f"Public ngrok URL: {public_url}")
    print(f"Scam Endpoint: {public_url}/scamHandling")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    run()