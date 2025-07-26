import requests
import os

# Use your ngrok public URL if running remotely
NGROK_BASE_URL = "https://1f8d235ed78b.ngrok-free.app/scamHandling"

def test_scam_call():
    payload = {
        "Scam": True,
        "ScamReason": "Caller claimed to be from the IRS demanding payment",
        "callTranscript": "Hello, this is the IRS. Please send your payment details."
    }

    response = requests.post(f"{NGROK_BASE_URL}/scamHandling", json=payload)
    assert response.status_code == 200
    print("✅ Scam call test passed")

def test_safe_call():
    payload = {
        "Scam": False,
        "ScamReason": "Caller identified themselves and asked about a prescription",
        "callTranscript": "Hi, I'm calling from the pharmacy to confirm your refill."
    }

    response = requests.post(f"{NGROK_BASE_URL}/scamHandling", json=payload)
    assert response.status_code == 200
    print("✅ Safe call test passed")

if __name__ == "__main__":
    test_scam_call()
    test_safe_call()