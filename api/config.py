import os
import chromadb

# Hugging Face token (if you need it for private models)
HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")

# Embedding Model: defaults to MiniLM if not set in .env or system env
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# LLM Server URL: defaults to localhost if not set in .env or system env
LLM_SERVER_URL = os.getenv("LLM_SERVER_URL", "http://llm-server:8001/completion")


# Configure ChromaDB with persistent storage (relative path, change if needed)
CHROMA_PATH = "./chroma_storage"
client = chromadb.PersistentClient(path=CHROMA_PATH)

# For simple projects: create/retrieve the default collection at import time
collection = client.get_collection(name="langchain")
