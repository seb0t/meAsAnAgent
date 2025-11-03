from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_google import ask_gemini

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_with_agent(req: ChatRequest):
    answer = ask_gemini(req.message)
    return {"response": answer}
