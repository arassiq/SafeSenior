from dotenv import load_dotenv
import requests
import json
from vapi import Vapi

client = Vapi(token=load_dotenv("VAPIAPIKEY"))

client.assistants.update(
    assistant_id="33ff19b0-33c6-4942-b579-3b454cc47f10",
    context="Scream everytime someone calls"
)