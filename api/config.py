import os

HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")

# Embedding Model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Change if needed

# Vector Database (using Chroma here as an example)
VECTOR_DB_NAME = "health_advice"  # Set to your collection name
