# api/api.py
# NOTE: All prompt and RAG logic is in api/chat.py.
# This file should only define API endpoints and call generate_response_with_context().

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils import extract_eva_response
from chat import generate_response_with_context

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    topic: str = "General"

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response_text = await generate_response_with_context(request.message, request.topic)
        eva_output = extract_eva_response(response_text)
        print(f"Request received: message='{request.message}', topic='{request.topic}'")
        print("Final cleaned response text sent to frontend:", eva_output["cleaned_text"])
        return JSONResponse(content={
            "response": eva_output["cleaned_text"],
            "blocks": eva_output["answer_blocks"],
            "raw": eva_output["raw"],  # optional: remove in prod for security/privacy
        })
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
    from embedding_search import retrieve_context_by_category
    try:
        context_texts = retrieve_context_by_category(request.message, request.topic)
        return JSONResponse(content={"context": context_texts})
    except Exception as e:
        print(f"Error during LLM test processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while testing the LLM.")
    