from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from api.embedding_search import retrieve_context_by_category
from api.chat import generate_response_with_context

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    topic: str = "General"

@router.post("/chat")
async def chat(request: ChatRequest):
    """Handles user chat requests by first retrieving similar content then generating a response."""
    try:
        # Retrieve context based on user query
        context_texts = retrieve_context_by_category(request.message, request.topic)
        context = " ".join(context_texts) if context_texts else "No relevant context found."
        
        # Generate response with context
        response_text = await generate_response_with_context(request.message, request.topic)
        print(f"Request received: message='{request.message}', topic='{request.topic}'")
        # Debugging log to verify final response text
        print("Final response text sent to frontend:", response_text)
        

        # Return response in JSON format for consistency
        return JSONResponse(content={"response": response_text})
    
    except Exception as e:
        # Error handling for backend failures
        print(f"Error during chat processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the chat request.")