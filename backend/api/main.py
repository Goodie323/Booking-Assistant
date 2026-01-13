from fastapi import FastAPI
from pydantic import BaseModel
from scripts.booking_chat_pipeline import chat

app = FastAPI(title="Booking Assistant API")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def health_check():
    return {"status": "Booking Assistant API is running"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    response = chat(request.message)
    return {"reply": response}
