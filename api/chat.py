import asyncio
import os
from langchain_core.prompts import PromptTemplate
# Fix the import
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from api.embedding_search import retrieve_context_by_category
from api.config import HF_TOKEN 

model_name = "microsoft/phi-2"  # Only 2.7GB, runs well on CPU
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # Regular precision for CPU
    device_map="cpu",  # Explicitly use CPU
)
# Create a pipeline and wrap it with LangChain
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.95,
    repetition_penalty=1.2,
)
llm = HuggingFacePipeline(pipeline=pipe)

# RAG-specific prompt that includes context
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are Eva, a virtual health assistant providing personalized advice. "
        "Use the following information to answer the user's question:\n\n"
        "REFERENCE INFORMATION:\n{context}\n\n"
        "USER QUESTION: {question}\n\n"
        "Provide a helpful response using the reference information."
    )
)

async def generate_response_with_context(input_text: str, topic: str = "General") -> str:
    try:
        # Retrieve context based on user input and topic
        context_texts = retrieve_context_by_category(query=input_text, category=topic)
        context = "\n".join(context_texts) if context_texts else "No specific information available on this topic."
        
        # Create prompt with context properly incorporated
        full_prompt = rag_prompt.format(context=context, question=input_text)
        
        # Generate response
        response = await asyncio.to_thread(llm.invoke, full_prompt)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm having trouble generating a response right now."
