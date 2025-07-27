from vapi_python import Vapi
from fastapi import FastAPI, Request, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import uvicorn
import os
import telnyx


from dotenv import load_dotenv
load_dotenv()

vapi = Vapi(api_key="YOUR_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def sendMessage(textMessage):
    telnyx.api_key = os.getenv("TELNYX_API_KEY")

    SENDER = os.getenv("TELYNXPHONENUMBER")      # E.164 format, e.g. "+15551234567"
    RECIPIENT = os.getenv("TELYNXRECIPIENT")     # E.164 format

    msg = telnyx.Message.create(
        from_=SENDER,      # note the trailing underscore to avoid Python's reserved 'from'
        to=RECIPIENT,
        text=textMessage,
        type="SMS"

    )
    print("Sent message ID:", msg.id)
    #print("Status:", msg.data['to'][0]['status'])  # delivery status



@app.post("/scamHandling")
async def scamHandling(request: Request):
    
    data = await request.json()
    if data["Scam"] == True:
        Message = sendText_Scam(data["ScamReason"], data["callTranscript"])
        print(f"Scam call, Message:\n{Message}")
    elif data["Scam"] == False:
        Message = sendText_SafeCall(data["ScamReason"], data["callTranscript"])
        print(f"Safe call, Message:\n{Message}")

    return {"status": "ok"}

def sendText_Scam(reason, transcript):
    Message = f"We have intercepted a call between a scammer and your elder\n\nReason for interception: {reason}\n\nTranscript: {transcript}"
    #sendMessage(Message)

    return Message

def sendText_SafeCall(reason, transcript):
    Message = f"We have approved a call between an unidentified number and your elder\n\nReason for approval: {reason}\n\nTranscript: {transcript}"
    #sendMessage(Message)

    return Message

def run():
    port = 8000
    public_url = ngrok.connect(port).public_url
    print(f"Public ngrok URL: {public_url}")
    print(f"Scam Endpoint: {public_url}/scamHandling")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    run()
    #sendText_Scam("Caller claimed to be from the IRS demanding payment", "Hello, this is the IRS. Please send your payment details.")