import os
import chromadb

HF_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN_WRITE")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
LLM_SERVER_URL = os.getenv("LLM_SERVER_URL", "http://eva-llama-cpp:8001/completion")

if os.getenv("IS_DOCKER", "false").lower() == "true":
    CHROMA_PATH = "/chroma_storage" # Path inside the Docker container
else:
    CHROMA_PATH = "./chroma_storage" # Path on the host machine for local scripts

client = chromadb.PersistentClient(path=CHROMA_PATH)