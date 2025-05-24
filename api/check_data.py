import chromadb
client = chromadb.PersistentClient(path="./chroma_storage")  # Or your path

for cname in ["langchain", "health_advice"]:
    col = client.get_collection(name=cname)
    print(f"[DEBUG] Collection '{cname}' doc count:", col.count())

from config import CHROMA_PATH, collection
import chromadb
print(f"[DEBUG] Using ChromaDB at: {CHROMA_PATH}")
client = chromadb.PersistentClient(path=CHROMA_PATH)
print(f"[DEBUG] Using collection: {collection.name}")