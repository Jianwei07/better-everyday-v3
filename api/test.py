import chromadb
client = chromadb.PersistentClient(path="./chroma_storage")  # Or /api/chroma_storage in container
collection = client.get_collection("langchain")  # or your collection name
docs = collection.get(limit=1, include=["embeddings"])
print(docs["embeddings"])



