from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    thread_id: str
    time_zone:str
