from fastapi import APIRouter
from pydantic import BaseModel
from api.chat import generate_response 
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    response_text = await generate_response(request.message)
    return {"response": response_text}
