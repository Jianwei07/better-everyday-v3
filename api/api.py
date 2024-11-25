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

class TestRequest(BaseModel):
    message: str
    topic: str

@router.post("/test_llm")
async def test_llm_endpoint(request: TestRequest):
    """Tests the LLM with static input based on the provided message and topic."""
    try:
        # Prepare the static input for testing
        context_texts = retrieve_context_by_category(request.message, request.topic)
        context = "\n".join(context_texts) if context_texts else "No relevant context found."
        
        # Construct the static input for LLM testing
        static_input = (
            f"User Query: {request.message}\n"
            f"Context:\n{context}\n"
            "Please provide a helpful response."
        )


        # Return response in JSON format for consistency
        return JSONResponse(content={"response": context_texts})

    except Exception as e:
        # Error handling for backend failures
        print(f"Error during LLM test processing: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while testing the LLM.")
