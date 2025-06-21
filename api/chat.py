import asyncio
import re
import traceback
from langchain_core.prompts import PromptTemplate
import httpx
from embedding_search import retrieve_context_by_category
from config import LLM_SERVER_URL
from utils import extract_eva_response  # modular output cleaner

RAG_PROMPT_TEMPLATE = """
You are Eva, an expert health assistant.
You answer questions based ONLY on the provided CONTEXT. If the context does not contain the answer, state that you cannot find the relevant information. Do not invent or speculate.

CONTEXT:
{context}

---

USER QUESTION: {question}

INSTRUCTIONS:
- Focus strictly on answering the USER QUESTION using ONLY the provided CONTEXT.
- If the user asks for host or guest names, search CONTEXT for their mention. If not present, reply: "The host or guest name is not available in the provided context."
- For all other questions, answer ONLY using CONTEXT. If the answer is not in CONTEXT, reply: "I don't know based on the provided context."
- Be concise and refer directly to CONTEXT.
- Start your response directly with the answer, without any introductory phrases, conversational turns, or follow-up questions.
- Do NOT repeat the user's question, your instructions, or the context in your answer.

Answer:
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question", "topic"],
    template=RAG_PROMPT_TEMPLATE,
)

DEFAULT_TIMEOUT = 120.0

async def call_llm_server(prompt: str) -> str:
    """Call the LLM server with error and timeout handling."""
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            payload = {
                "prompt": prompt,
                "max_tokens": 150, # Example: Reduce to encourage conciseness
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["\nAnswer:", "\nQUESTION:", "---", "\nINSTRUCTIONS:", "\nCONTEXT:", "RESPONSE:", "\nRevised Answer:"], # Add the new stop for self-reflection
            }
            response = await client.post(LLM_SERVER_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            print(f"[Eva-RAG DEBUG] LLM raw API response: {data}")

            llm_content = None
            if isinstance(data, dict):
                if "content" in data:
                    llm_content = data["content"]
                elif "choices" in data and data["choices"]:
                    choice = data["choices"][0]
                    llm_content = (
                        choice.get("text")
                        or choice.get("generated_text")
                        or choice.get("content")
                    )
                elif "generated_text" in data:
                    llm_content = data["generated_text"]
                elif "text" in data:
                    llm_content = data["text"]
            
            # CRITICAL FIX 1: Guarantee the return type is a string
            # No matter what llm_content or data is, this *must* be a string.
            if not isinstance(llm_content, str):
                print(f"[Eva-RAG WARNING] LLM content not found in expected keys or not string. Data type: {type(data)}. Full data: {data}")
                return str(data) # Force conversion, this is where the error should be caught if it's not a str

            return llm_content

    except httpx.ReadTimeout:
        print("[Eva-RAG ERROR] LLM server timed out.")
        return "Sorry, the AI model took too long to respond. Please try again!"
    except Exception as e:
        print(f"[Eva-RAG ERROR] Exception in LLM call: {e}")
        traceback.print_exc()
        return "Sorry, there was a problem contacting the AI model."

async def self_reflect_on_answer(context: str, answer: str) -> str:
    """
    Calls the LLM to reflect on and critique its own answer.
    Returns a revised answer if the original wasn't grounded in context.
    """
    prompt = (
        "CONTEXT:\n" # Simpler marker
        f"{context}\n\n"
        "ORIGINAL RESPONSE:\n" # Simpler marker
        f"{answer}\n\n"
        "INSTRUCTIONS:\n"
        "Analyze the 'ORIGINAL RESPONSE' based ONLY on the 'CONTEXT'.\n"
        "1. If the 'ORIGINAL RESPONSE' is fully supported by the 'CONTEXT', output the 'ORIGINAL RESPONSE' verbatim.\n"
        "2. If parts of the 'ORIGINAL RESPONSE' are NOT supported by the 'CONTEXT', revise it to include ONLY information found in the 'CONTEXT'.\n"
        "3. If nothing in the 'ORIGINAL RESPONSE' is supported by the 'CONTEXT', state: 'I don't know based on the provided context.'\n"
        "4. Be concise and direct. Do NOT include any introductory phrases, conversational elements, or disclaimers like 'Based on the context,'.\n"
        "5. Do NOT repeat these INSTRUCTIONS, the CONTEXT, or the ORIGINAL RESPONSE in your output.\n"
        "6. Provide ONLY the revised answer (or the 'I don't know' statement).\n"
        "Revised Answer:" # Clear final marker
    )
    # The call_llm_server function handles the stop tokens.
    return await call_llm_server(prompt)

def is_generic_or_empty(text: str) -> bool:
    """
    Detects obviously generic or non-contextual LLM outputs after initial cleaning.
    """
    cleaned_text = text.strip().lower() # Work with lowercased, stripped text
    
    if not cleaned_text:
        return True
    
    # Common generic starts
    generic_starts = [
        "thank you for your question", "i'm an ai", "as an ai", "i'm sorry",
        "i do not have enough information", "based on my knowledge", "hi there"
    ]
    for phrase in generic_starts:
        if cleaned_text.startswith(phrase.lower()):
            return True
            
    # LLM sometimes outputs a generic "no info" answer
    if "i don't know" in cleaned_text or "not available in the provided context" in cleaned_text:
        return True
        
    # If the LLM generates only empty markdown headers or other specific non-answer patterns
    # after extract_eva_response has run
    if re.fullmatch(r"^(#+\s*.*?\n*)*\s*$", cleaned_text, re.DOTALL | re.IGNORECASE):
        return True

    # If the LLM just echoes parts of the prompt despite instructions (more aggressive check)
    # Check for short responses that are clearly just prompt echoes
    if len(cleaned_text.split()) < 10: # If very short
        if "user question:" in cleaned_text or "context:" in cleaned_text or "instructions:" in cleaned_text or "answer:" in cleaned_text or "response:" in cleaned_text:
            return True

    return False

def fallback_response(context_list, topic):
    bullets = "\n".join([f"- {point}" for point in context_list])
    return (
        f"Here are practical recommendations for {topic}:\n"
        f"{bullets}\n"
        "Let me know if you need more details!"
    )

# Main function to generate a response using RAG
async def generate_response_with_context(input_text: str, topic: str = "General") -> dict:
    """
    Main RAG orchestration:
    1. Retrieves context docs
    2. Calls LLM to generate answer
    3. Calls LLM a second time to self-reflect and refine answer
    4. Returns structured result for API/UI
    """
    try:
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        if not context_texts or context_texts == ["No specific advice available for this topic."]:
            fallback = "I don't know based on the provided context."
            # Ensure string input here too
            return extract_eva_response(str(fallback)) # Always cast to str here

        context = "\n".join(context_texts)
        prompt = rag_prompt.format(context=context, question=input_text, topic=topic)

        try:
            # Primary LLM call
            response = await asyncio.wait_for(
                call_llm_server(prompt),
                timeout=DEFAULT_TIMEOUT,
            )
            # CRITICAL FIX 2: Ensure 'response' is a string before passing to is_generic_or_empty or self_reflect_on_answer
            if not isinstance(response, str):
                print(f"[Eva-RAG ERROR] Primary LLM call returned non-string type ({type(response)}). Forcing to string for processing.")
                response = str(response) # Force conversion

            if is_generic_or_empty(response):
                reflected = "I don't know based on the provided context."
            else:
                # Self-reflection LLM call (for final grounding)
                reflected = await asyncio.wait_for(
                    self_reflect_on_answer(context, response),
                    timeout=DEFAULT_TIMEOUT,
                )
            
            # CRITICAL FIX 3: Ensure 'reflected' is a string before passing to extract_eva_response
            if not isinstance(reflected, str):
                print(f"[Eva-RAG ERROR] Self-reflection LLM call returned non-string type ({type(reflected)}). Forcing to string for final extraction.")
                reflected = str(reflected)

            return extract_eva_response(reflected)
        except asyncio.TimeoutError:
            print("[Eva-RAG ERROR] Overall async timeout.")
            # Ensure string input here too
            return extract_eva_response(str(fallback_response(context_texts, topic)))
    except Exception as e:
        print(f"[Eva-RAG ERROR]: {e}")
        # THIS IS THE MOST IMPORTANT DEBUG STEP NOW: Print full traceback
        traceback.print_exc() # Ensure this is working to give full traceback for new errors
        # Ensure string input here too
        return extract_eva_response(str("Sorry, I'm having trouble processing your request. Please try again soon."))

# CLI manual test (optional)
if __name__ == "__main__":
    import sys
    import time
    query = sys.argv[1] if len(sys.argv) > 1 else "How do I improve my brain health?"
    topic = sys.argv[2] if len(sys.argv) > 2 else "Neuro"
    loop = asyncio.get_event_loop()
    start = time.time()
    answer = loop.run_until_complete(generate_response_with_context(query, topic))
    print("\nEva's answer:\n", answer["cleaned_text"])
    print("\nBlocks:", answer["answer_blocks"])
    print(f"\nTotal pipeline time: {time.time() - start:.2f} seconds")
