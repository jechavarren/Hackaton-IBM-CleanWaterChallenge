from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    score: int 
    question: str 
    answer: str 
    valoration: str 
