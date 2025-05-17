# api/api.py
# NOTE: All prompt and RAG logic is in api/chat.py.
# This file should only define API endpoints and call generate_response_with_context().

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from api.chat import generate_response_with_context

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    topic: str = "General"

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Handles user chat requests: calls the RAG generator in chat.py and returns the response.
    """
    try:
        response_text = await generate_response_with_context(request.message, request.topic)
        print(f"Request received: message='{request.message}', topic='{request.topic}'")
        print("Final response text sent to frontend:", response_text)
        return JSONResponse(content={"response": response_text})

    except Exception as e:
        print(f"Error during chat processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the chat request.")

# (Optional) Simple endpoint to see retrieved context (for debugging, not user-facing)
class TestRequest(BaseModel):
    message: str
    topic: str

@router.post("/test_llm")
async def test_llm_endpoint(request: TestRequest):
    """
    Debug endpoint: returns retrieved context from the vector DB (does NOT run LLM).
    """
    from api.embedding_search import retrieve_context_by_category
    try:
        context_texts = retrieve_context_by_category(request.message, request.topic)
        return JSONResponse(content={"context": context_texts})
    except Exception as e:
        print(f"Error during LLM test processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while testing the LLM.")
