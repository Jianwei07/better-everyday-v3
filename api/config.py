import os
import chromadb

# Configure ChromaDB with persistent storage
client = chromadb.PersistentClient(path="./chroma_storage")

# Create or retrieve the collection
collection = client.get_or_create_collection(name="health_advice")

# Hugging Face token (if needed)
HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")

# Embedding Model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
