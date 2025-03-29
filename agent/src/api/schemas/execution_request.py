from typing import Optional
from pydantic import BaseModel


class InferenceMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    current_message_id: Optional[str] = None
    previous_message_id: Optional[str] = None
    metadata: dict = {}


class ExecutionRequest(BaseModel):
    sampling_point: str = '123'
    metadata: dict = {}


class ExecutionResponse(BaseModel):
    message: str = "Ejecución correcta"
    metadata: dict = {}
