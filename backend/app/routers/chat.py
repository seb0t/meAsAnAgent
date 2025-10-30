# endpoint chat

from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(message: str):
    # TODO: implement chat logic
    print("hello world")
    print(message.capitalize())
    return {"response": f"Hello from AI Career Agent - - {message.capitalize()}"}