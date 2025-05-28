from pydantic import BaseModel
from typing import Dict, Optional

class NotificationPayload(BaseModel):
    title: str
    body: str
    data: Optional[Dict] = {}
    image_url: Optional[str] = None
    action_url: Optional[str] = None
