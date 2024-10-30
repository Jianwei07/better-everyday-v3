import asyncio
import os
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from api.embedding_search import retrieve_similar_texts  # Import for context retrieval
from api.config import HF_TOKEN  # Ensure config.py has the HF_TOKEN

# Configure the Flan-T5 model as a text-to-text endpoint
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-base",  # Changed to Flan-T5
    task="text2text-generation",
    max_new_tokens=150,
    do_sample=True,
    temperature=0.2,
    top_p=0.9,
    repetition_penalty=1.2,
    huggingfacehub_api_token=HF_TOKEN,
)

# Define prompt template for conversational health advice
prompt = PromptTemplate(
    input_variables=["input"],
    template=(
        "You are Eva, a virtual health assistant providing focused, concise advice. "
        "Answer user questions with practical health tips only.\n\n"
        "User: {input}\nAssistant:"
    )
)

# Function to clean the generated response
def clean_response(response_text):
    if not response_text.endswith((".", "!", "?")):
        last_period = response_text.rfind(".")
        if last_period != -1:
            response_text = response_text[:last_period + 1]  # Trim to last full sentence
    return response_text.strip()

async def generate_response_with_context(input_text: str, topic: str = "General") -> str:
    try:
        # Use the embedding model to retrieve relevant context
        topic_intro = {
            "Eye Health": "Provide health advice on eye health.",
            "Neuro": "Provide brain health tips to improve cognition.",
            "Cancer Prevention": "Provide advice on cancer prevention.",
            "Strength and Weights Training": "Give tips for effective strength and weights training.",
            "Fat Loss": "Provide fat loss advice for health.",
            "Random Advice": "Give a random health tip.",
            "Quick Tips": "Share a quick, motivational health tip."
        }

        # Retrieve similar advice texts from embedding search based on input query
        context_texts = retrieve_similar_texts(input_text)
        context = " ".join(context_texts)  # Combine retrieved texts as context

        # Combine context with prompt for Flan-T5
        adjusted_input = f"{topic_intro.get(topic, 'General wellness advice')}\nContext: {context}\nUser: {input_text}"

        # Use Flan-T5 for response generation with the added context
        raw_response = await asyncio.to_thread(llm.invoke, {"input": adjusted_input})

        # Extract and clean up the response text
        response_text = raw_response if isinstance(raw_response, str) else raw_response.get("text", "I'm here to help with health-related advice!")
        response_text = clean_response(response_text)

        # Further trim the response if it’s too long
        if len(response_text.split()) > 50:
            response_text = ". ".join(response_text.split(".")[:2]) + "."

        print("Generated response:", response_text)  # For debugging
        return response_text
    except Exception as e:
        print(f"Error during response generation: {e}")
        return "I'm having trouble generating a response right now."
