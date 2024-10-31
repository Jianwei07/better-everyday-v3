from fastapi import APIRouter
from pydantic import BaseModel
from api.embedding_search import retrieve_context_by_category
from api.chat import generate_response_with_context

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    topic: str = "General"

@router.post("/chat")
async def chat(request: ChatRequest):
    """Handles user chat requests by first retrieving similar content then generating a response."""
    # Retrieve context based on user query
    context_texts = retrieve_context_by_category(request.message)
    context = " ".join(context_texts)
    
    # Generate response with context
    response_text = await generate_response_with_context(request.message, context)
    
    return {"response": response_text}
