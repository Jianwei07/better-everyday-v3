from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME,collection

# Initialize embedding model and vector database client
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def retrieve_context_by_category(query, category, top_k=3):
    # Encode the query into an embedding
    query_embedding = embedding_model.encode([query])[0]

    # Perform a search with category filtering and specify fields to include in results
    results = collection.query(
        query_embeddings=[query_embedding],
        where={"category": category},
        include=["documents", "metadatas", "distances"]
    )
    
    # Debugging statements
    print("Query embedding:", query_embedding)
    print("Category filter:", category)
    print("Raw query results:", results)

    # Check if the query returned valid documents
    if not results.get("documents") or not results["documents"][0]:
        print("No relevant documents found for the query.")
        print("Raw query results:", results)
        return ["No specific advice available for this topic."]

    # Extract and return the text content from documents, limited to top_k results
    return [doc for doc in results["documents"][0][:top_k]]
