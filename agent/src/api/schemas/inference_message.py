from typing import Optional
from pydantic import BaseModel


class InferenceMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    current_message_id: Optional[str] = None
    previous_message_id: Optional[str] = None
    metadata: dict = {}


class InferenceRequest(InferenceMessage):
    message: str 
    metadata: dict 


class InferenceResponse(InferenceMessage):
    message: str 
    metadata: dict 
