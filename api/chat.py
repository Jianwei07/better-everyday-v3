import asyncio
import os
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from api.embedding_search import retrieve_context_by_category  # Updated import for category-specific retrieval
from api.config import HF_TOKEN  # Ensure config.py has the HF_TOKEN

# Configure the Flan-T5 model as a text-to-text endpoint
llm = HuggingFaceEndpoint(
    repo_id="distilbert/distilgpt2",  # Changed to Flan-T5
    task="text-generation",
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

def clean_response(response_text):
    response_text = response_text.strip()
    if len(response_text.split()) > 50:  # Limit to 50 words, customize as needed
        response_text = ". ".join(response_text.split(".")[:2]) + "."
    return response_text

async def generate_response_with_context(input_text: str, topic: str = "General") -> str:
    try:
        # Topic-specific introductory prompts for context
        topic_prompts = {
            "Eye Health": "Please provide specific advice for improving eye health.",
            "Neuro": "Please provide specific advice for improving brain health.",
            "Cancer Prevention": "Please provide specific advice on reducing cancer risk.",
            "Strength and Weights Training": "Please provide specific advice on effective muscle building.",
            "Fat Loss": "Please provide specific advice on safe fat loss strategies.",
            "Random Advice": "Please provide random health advice.",
            "Quick Tips": "Share a quick, motivational health tip."
        }
        
        # Retrieve the introductory prompt for the selected topic
        topic_prompt = topic_prompts.get(topic)

        # Retrieve category-specific context based on user input and selected topic
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        if context_texts and isinstance(context_texts, list):
            context = "\n".join(context_texts)  # Removed bullet points for simplicity
        else:
            context = "No specific advice available for this topic."

        # Combine topic prompt, context, and user input for the LLM's adjusted input
        adjusted_input = (
            f"{topic_prompt}\n\n"
            f"Here are some specific health tips related to {topic}:\n"
            f"{context}\n\n"
            f"User Query: {input_text}\n\n"
            "Please respond with advice or suggestions based on the provided context."
        )
        print("Adjusted input sent to LLM:", adjusted_input)

        # Invoke the language model to generate a response
        raw_response = await asyncio.to_thread(llm.invoke, adjusted_input)

        # Extract and clean up the response text
        if not raw_response or not isinstance(raw_response, str):
            print("Warning: Received empty response from LLM.")
            response_text = "I'm here to help with health-related advice! Feel free to ask specific questions."
        else:
            response_text = clean_response(raw_response)

        # Print the final response for debugging
        print("Final response text sent to frontend:", response_text)
        return response_text
    except Exception as e:
        print(f"Error during response generation: {e}")
        return "I'm having trouble generating a response right now."
