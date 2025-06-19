from sentence_transformers import SentenceTransformer
# Import client, not collection, and embedding_functions for Chroma
from config import EMBEDDING_MODEL_NAME, client
import chromadb.utils.embedding_functions as embedding_functions

# Initialize the embedding model once for query embedding
query_embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Define a consistent embedding function for ChromaDB to use if it's creating/getting collections
# This ensures Chroma knows how to handle embeddings if you add text directly
# IMPORTANT: This must match what you use in your ingestion script if you use Chroma's auto-embedding.
chroma_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL_NAME
)

def retrieve_context_by_category(query, category, top_k=3):
    category = category.strip().lower() # Ensure consistent casing for collection names
    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Category (used for filter): '{category}'")

    try:
        # Get or create the topic-specific collection
        current_collection = client.get_or_create_collection(
            name=category, # Collection name is now the topic/category (e.g., "neuro")
            embedding_function=chroma_embedding_function # Pass the embedding function
        )
    except Exception as e:
        print(f"[ERROR] Could not get/create collection '{category}': {e}")
        return ["Error: Could not access topic-specific database."]

    print(f"[DEBUG] Using ChromaDB collection: '{current_collection.name}'")

    # (Corrected) Print all unique categories stored in Chroma (meta debugging)
    try:
        # Fetch metadatas from the specific collection being queried
        all_doc_data = current_collection.get(limit=current_collection.count(), include=["metadatas"])
        all_metadatas_list = all_doc_data.get("metadatas", []) # This is a list of dicts

        categories_in_collection = set()
        for meta in all_metadatas_list: # Iterate directly over the list of metadata dictionaries
            if meta and "category" in meta:
                categories_in_collection.add(meta["category"])
        print(f"[DEBUG] All unique 'category' metadatas in collection '{category}': {categories_in_collection}")
    except Exception as e:
        print(f"[DEBUG] Could not fetch all metadatas from collection '{category}': {e}")


    # Embed the query using the same model
    query_embedding = query_embedding_model.encode([query]).tolist()[0] # .tolist() to ensure serializable if needed

    # The where_filter is still useful to filter within the collection, though redundant if collection is topic-specific
    where_filter = {"category": category}
    print(f"[DEBUG] Chroma WHERE filter: {where_filter}")

    results = current_collection.query(
        query_embeddings=[query_embedding],
        where=where_filter,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    print(f"[DEBUG] Raw query results: {results}")

    if not results.get("documents") or not results["documents"][0]:
        print("[DEBUG] No relevant documents found for the query.")
        return ["No specific advice available for this topic."]

    print("[DEBUG] Retrieved docs:")
    # Ensure there are actually documents to iterate
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0][:top_k]):
            print(f"  Doc {i}: {doc[:200]}...")
    else:
        print("[DEBUG] Documents list is empty after query, despite initial check.")

    return [doc for doc in results["documents"][0][:top_k]]