from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME, collection

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def retrieve_context_by_category(query, category, top_k=3):
    category = category.strip().lower()
    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Category (used for filter): '{category}'")
    query_embedding = embedding_model.encode([query])[0]

    # (NEW) Print all unique categories stored in Chroma (meta debugging)
    try:
        # Get all metadata for all docs (may be slow if DB is huge)
        all_metadatas = collection.get(include=["metadatas"])["metadatas"]
        categories = set()
        for meta in all_metadatas[0]:
            if meta and "category" in meta:
                categories.add(meta["category"])
        print(f"[DEBUG] All unique categories in Chroma: {categories}")
    except Exception as e:
        print(f"[DEBUG] Could not fetch all metadatas: {e}")

    where_filter = {"category": category}
    print(f"[DEBUG] Chroma WHERE filter: {where_filter}")

    results = collection.query(
        query_embeddings=[query_embedding],
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    print(f"[DEBUG] Raw query results: {results}")

    if not results.get("documents") or not results["documents"][0]:
        print("[DEBUG] No relevant documents found for the query.")
        return ["No specific advice available for this topic."]

    print("[DEBUG] Retrieved docs:")
    for i, doc in enumerate(results["documents"][0][:top_k]):
        print(f"  Doc {i}: {doc[:200]}...")  # Print only first 200 chars for readability

    return [doc for doc in results["documents"][0][:top_k]]
