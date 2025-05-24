import asyncio
import traceback
from langchain_core.prompts import PromptTemplate
import httpx
from embedding_search import retrieve_context_by_category
from config import LLM_SERVER_URL
from utils import extract_eva_response  # modular output cleaner

RAG_PROMPT_TEMPLATE = """
You are Eva, an expert health assistant.
You answer questions based only on the provided CONTEXT, which comes from podcast transcripts or summaries.

CONTEXT:
{context}

---

USER QUESTION: {question}

INSTRUCTIONS:
- If the user's question asks for host or guest names, search CONTEXT for their mention. If not present, reply: "The host or guest name is not available in the provided context."
- For all other questions, answer ONLY using CONTEXT.
- If the answer is not in CONTEXT, reply: "I don't know based on the provided context."
- Never invent or speculate. Be concise and refer directly to CONTEXT.

RESPONSE:
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question", "topic"],
    template=RAG_PROMPT_TEMPLATE,
)

DEFAULT_TIMEOUT = 30.0  # To allow for self-reflection if needed

async def call_llm_server(prompt: str) -> str:
    """Call the LLM server with error and timeout handling."""
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            payload = {
                "prompt": prompt,
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["\nRESPONSE:"],
            }
            response = await client.post(LLM_SERVER_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            print(f"[Eva-RAG DEBUG] LLM raw API response: {data}")

            # Standard LLM output parsing (robust for different APIs)
            if isinstance(data, dict):
                if "content" in data:
                    return data["content"]
                if "choices" in data and data["choices"]:
                    choice = data["choices"][0]
                    return (
                        choice.get("text")
                        or choice.get("generated_text")
                        or choice.get("content")
                    )
                if "generated_text" in data:
                    return data["generated_text"]
                if "text" in data:
                    return data["text"]
            return str(data)
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
        "CONTEXT:\n"
        f"{context}\n\n"
        "ANSWER:\n"
        f"{answer}\n\n"
        "INSTRUCTIONS:\n"
        "Reflect on the above answer. Is it fully supported by the context? "
        "If not, revise the answer to only use information found in context. "
        "If nothing relevant is found, say: 'I don't know based on the provided context.'\n\n"
        "RESPONSE:"
    )
    return await call_llm_server(prompt)

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
            return extract_eva_response(fallback)

        context = "\n".join(context_texts)
        prompt = rag_prompt.format(context=context, question=input_text, topic=topic)

        try:
            # Primary LLM call
            response = await asyncio.wait_for(
                call_llm_server(prompt),
                timeout=DEFAULT_TIMEOUT,
            )
            # If the LLM response is obviously generic, trigger stricter self-reflection
            if is_generic_or_empty(response):
                reflected = "I don't know based on the provided context."
            else:
                # Self-reflection LLM call (for final grounding)
                reflected = await asyncio.wait_for(
                    self_reflect_on_answer(context, response),
                    timeout=DEFAULT_TIMEOUT,
                )
            return extract_eva_response(reflected)
        except asyncio.TimeoutError:
            print("[Eva-RAG ERROR] Overall async timeout.")
            return extract_eva_response(fallback_response(context_texts, topic))
    except Exception as e:
        print(f"[Eva-RAG ERROR]: {e}")
        traceback.print_exc()
        return extract_eva_response("Sorry, I'm having trouble processing your request. Please try again soon.")

def is_generic_or_empty(text: str) -> bool:
    """
    Detects obviously generic or non-contextual LLM outputs.
    Add your own rules as needed.
    """
    if not text or text.strip() == "":
        return True
    generic_starts = [
        "Thank you for your question", "I'm an AI", "As an AI", "I'm sorry",
        "I do not have enough information", "Based on my knowledge", "Hi there"
    ]
    for phrase in generic_starts:
        if text.strip().lower().startswith(phrase.lower()):
            return True
    # LLM sometimes outputs a generic "no info" answer
    if "I don't know" in text or "not available in the provided context" in text:
        return True
    return False

def fallback_response(context_list, topic):
    bullets = "\n".join([f"- {point}" for point in context_list])
    return (
        f"Here are practical recommendations for {topic}:\n"
        f"{bullets}\n"
        "Let me know if you need more details!"
    )

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
