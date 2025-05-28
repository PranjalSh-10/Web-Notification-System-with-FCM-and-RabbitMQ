from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from publisher import publish_notification
import json
import os
import asyncio

from models import NotificationPayload
from publisher import publish_notification

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Live Server
    "http://localhost:5500"   # Just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOKENS_FILE = "tokens.json"

# Load tokens from file or initialize empty list
if os.path.exists(TOKENS_FILE):
    with open(TOKENS_FILE, "r") as f:
        registered_tokens = json.load(f)
else:
    registered_tokens = []

class DeviceToken(BaseModel):
    fcm_token: str

@app.post("/devices/register")
def register_device(device: DeviceToken):
    if device.fcm_token not in registered_tokens:
        registered_tokens.append(device.fcm_token)
        with open(TOKENS_FILE, "w") as f:
            json.dump(registered_tokens, f)
        return {"message": "Token registered successfully"}
    else:
        return {"message": "Token already registered"}

@app.post("/notifications/publish")
async def publish(payload: NotificationPayload):
    try:
        await publish_notification(payload.dict())
        return {"message": "Notification published"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))