import asyncio
import traceback
from langchain_core.prompts import PromptTemplate
import httpx
from embedding_search import retrieve_context_by_category
from config import LLM_SERVER_URL

# Prompt template (subject-aware)
RAG_PROMPT_TEMPLATE = """
You are Eva, a warm and knowledgeable health assistant focused on the topic of "{topic}".
Answer the USER QUESTION below based only on the provided CONTEXT. Do not make up information or speculate.

CONTEXT:
{context}

---

USER QUESTION: {question}

INSTRUCTIONS:
- Directly answer the question using only the information in CONTEXT.
- Organize your answer clearly (paragraphs or bullets).
- Use an encouraging, actionable, but concise tone.

RESPONSE:
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question", "topic"],
    template=RAG_PROMPT_TEMPLATE,
)

async def call_llm_server(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
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
        print(f"[Eva-RAG DEBUG] LLM raw API response: {data}")  # Debug print

        if isinstance(data, dict):
            if "content" in data:
                return data["content"]
            if "choices" in data and data["choices"]:
                choice = data["choices"][0]
                return choice.get("text") or choice.get("generated_text") or choice.get("content")
            if "generated_text" in data:
                return data["generated_text"]
            if "text" in data:
                return data["text"]
        return str(data)

async def generate_response_with_context(input_text: str, topic: str = "General") -> str:
    try:
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        if not context_texts:
            return f"I couldn't find any reliable information on {topic} yet, but let me know if you want advice on a different health topic!"

        context = "\n".join(context_texts)
        prompt = rag_prompt.format(context=context, question=input_text, topic=topic)

        try:
            response = await asyncio.wait_for(
                call_llm_server(prompt),
                timeout=12.0
            )
            return extract_response(response)
        except asyncio.TimeoutError:
            return fallback_response(context_texts, topic)
    except Exception as e:
        print(f"[Eva-RAG ERROR]: {e}")
        traceback.print_exc()
        return "Sorry, I'm having trouble processing your request. Please try again soon."

def extract_response(response: str) -> str:
    if "RESPONSE:" in response:
        return response.split("RESPONSE:")[-1].strip()
    return response.strip()

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
    query = sys.argv[1] if len(sys.argv) > 1 else "How do I improve my brain health?"
    topic = sys.argv[2] if len(sys.argv) > 2 else "Neuro"
    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(generate_response_with_context(query, topic))
    print("\nEva's answer:\n", answer)
