import asyncio
import os
from langchain_core.prompts import PromptTemplate
# Fix the import
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from api.embedding_search import retrieve_context_by_category
from api.config import HF_TOKEN 
import re

model_name = "microsoft/phi-2"  # Only 2.7GB, runs well on CPU
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # Regular precision for CPU
    device_map="cpu",  # Explicitly use CPU
)
# Optimize the phi-2 model to respond faster
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,  # Increased from 100 to allow longer responses
    temperature=0.7,     # Slightly higher for more creative responses
    top_p=0.9,
    repetition_penalty=1.1,  # Reduced to allow some natural repetition
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id,
    num_return_sequences=1,
)
llm = HuggingFacePipeline(pipeline=pipe)

# Create much simpler prompt template
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are Eva, a knowledgeable health assistant providing personalized advice.\n\n"
        "REFERENCE INFORMATION:\n{context}\n\n"
        "USER QUESTION: {question}\n\n"
        "Instructions: Provide a detailed, helpful response that:\n"
        "1. Directly answers the question\n"
        "2. Incorporates ALL the reference information\n"
        "3. Adds explanations for why these recommendations work\n"
        "4. Organizes information in clear paragraphs or bullet points\n"
        "5. Uses a warm, encouraging tone\n\n"
        "RESPONSE:"
    )
)

# Add custom timeout handling that uses retrieved context
async def generate_response_with_context(input_text: str, topic: str = "General") -> str:
    try:
        # Get context first
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        if not context_texts:
            return "I don't have specific information on that topic yet, but I'd be happy to help with other health questions."
        
        context = "\n".join(context_texts)
        
        # Create prompt with context
        full_prompt = rag_prompt.format(context=context, question=input_text)
        
        # Try to generate with a reasonable timeout
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(llm.invoke, full_prompt),
                timeout=10.0  # Increased to 10 seconds for more elaborate responses
            )
            return extract_model_response(response)
        except asyncio.TimeoutError:
            # Create an enhanced fallback response using the retrieved context
            return create_enhanced_fallback(input_text, context_texts)
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I apologize, but I'm having trouble processing that request right now. Please try again in a moment."

def create_enhanced_fallback(question: str, context_texts: list) -> str:
    """Create a more detailed fallback response when model times out."""
    topic = question.lower().replace("?", "").replace("how", "").replace("can", "").replace("do", "").replace("i", "").strip()
    
    intro = f"Here's what health experts recommend about {topic}:"
    
    # Format each point as a bullet with slight elaboration
    bullet_points = []
    for i, point in enumerate(context_texts):
        # Add simple elaborations based on common health advice patterns
        if "diet" in point.lower() or "eat" in point.lower() or "food" in point.lower():
            bullet_points.append(f"• {point} This provides essential nutrients your body needs.")
        elif "exercise" in point.lower() or "physical" in point.lower() or "activity" in point.lower():
            bullet_points.append(f"• {point} Regular activity improves overall health outcomes.")
        elif "sleep" in point.lower() or "rest" in point.lower():
            bullet_points.append(f"• {point} Quality sleep is crucial for recovery and proper function.")
        else:
            bullet_points.append(f"• {point}")
    
    conclusion = "Incorporating these practices consistently will help you see the best results."
    
    return f"{intro}\n\n" + '\n'.join(bullet_points) + f"\n\n{conclusion}"

async def _generate_response(input_text: str, topic: str) -> str:
    try:
        # Retrieve context based on user input and topic
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        context = "\n".join(context_texts) if context_texts else "No specific information available on this topic."
        
        # Create prompt with context properly incorporated
        full_prompt = rag_prompt.format(context=context, question=input_text)
        
        # Generate response
        full_response = await asyncio.to_thread(llm.invoke, full_prompt)
        
        # Clean up the response to extract only the generated part
        clean_response = extract_model_response(full_response)
        
        return clean_response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm having trouble generating a response right now."

def extract_model_response(response: str) -> str:
    """Extract just the model's response from the full output."""
    # Look for the output marker
    if "OUTPUT:" in response:
        return response.split("OUTPUT:")[1].strip()
    
    # If no marker, look for the end of the prompt template
    prompt_end_markers = [
        "Provide a helpful response using the reference information.",
        "USER QUESTION:",
        "REFERENCE INFORMATION:"
    ]
    for marker in prompt_end_markers:
        if marker in response:
            parts = response.split(marker)
            if len(parts) > 1 and parts[-1].strip():
                # Find the first complete sentence after the last marker
                content = parts[-1].strip()
                # Skip any initial instructions or non-sentences
                first_sentence_start = re.search(r'[A-Z][^.!?]*[.!?]', content)
                if first_sentence_start:
                    return content[first_sentence_start.start():].strip()
                return content
    # Fallback - return everything after the last line of the prompt template
    lines = response.strip().split('\n')
    if len(lines) > 1:
        return '\n'.join(lines[1:]).strip()
    
    return response.strip()
