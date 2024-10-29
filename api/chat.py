import asyncio
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")

# Configure Hugging Face Endpoint with adjusted parameters for health-specific responses
llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3.5-mini-instruct",
    task="text-generation",
    max_new_tokens=80,
    do_sample=True,
    temperature=0.2,
    top_p=0.85,
    repetition_penalty=1.5,
    huggingfacehub_api_token=hf_token,
)

prompt = PromptTemplate(
    input_variables=["input"],
    template=(
        "You are Eva, a virtual health assistant providing focused, concise advice. "
        "Answer user questions with practical health tips only. Do not introduce yourself, "
        "do not explain your background, and do not mention Phi Beta Kappa or any credentials.\n\n"
        "User: {input}\nAssistant:"
    )
)
# Initialize LLMChain with the prompt and model
chat_chain = prompt | llm | StrOutputParser()

def clean_response(response_text):
    # Ensure response ends on a complete sentence
    if not response_text.endswith((".", "!", "?")):
        last_period = response_text.rfind(".")
        if last_period != -1:
            response_text = response_text[:last_period + 1]  # Trim to last full sentence
    return response_text

async def generate_response(input_text: str, topic: str = "General") -> str:
    try:
        # Modify the input based on topic for focused responses
        topic_intro = {
            "Eye Health": "Provide health advice on eye health.",
            "Neuro": "Provide brain health tips to improve cognition.",
            "Cancer Prevention": "Provide advice on cancer prevention.",
            "Strength and Weights Training": "Give tips for effective strength and weights training.",
            "Fat Loss": "Provide fat loss advice for health.",
            "Random Advice": "Give a random health tip.",
            "Quick Tips": "Share a quick, motivational health tip."
        }

        # Concatenate topic intro with user input for context
        adjusted_input = f"{topic_intro.get(topic, 'General wellness advice')}\nUser: {input_text}"
        
        # Invoke the model synchronously in an async context
        raw_response = await asyncio.to_thread(chat_chain.invoke, {"input": adjusted_input})

        # Check if the response is a string or dictionary, handle accordingly
        response_text = raw_response if isinstance(raw_response, str) else raw_response.get("text", "I'm here to help with health-related advice!")
        
        # Clean up and trim overly verbose answers
        response_text = clean_response(response_text)
        
        # Further trim the response if it exceeds 50 words (adjustable threshold)
        if len(response_text.split()) > 50:
            response_text = ". ".join(response_text.split(".")[:2]) + "."

        print("Generated response:", response_text)  # For debugging
        return response_text
    except Exception as e:
        print(f"Error during response generation: {e}")
        return "I'm having trouble generating a response right now."
