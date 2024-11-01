from sentence_transformers import SentenceTransformer
import chromadb
from api.config import EMBEDDING_MODEL_NAME, VECTOR_DB_NAME

# Initialize embedding model and vector database client
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
client = chromadb.Client()
collection = client.get_or_create_collection(VECTOR_DB_NAME)

def add_data_with_metadata(texts, category):
    """
    Add health advice data to the vector database with metadata for category filtering.
    
    Args:
        texts (list): List of strings containing health advice.
        category (str): Category tag for the health advice (e.g., "Eye Health").
    """
    embeddings = embedding_model.encode(texts)
    
     # Generate unique IDs for each document
    ids = [f"{category}_text_{i}" for i in range(len(texts))]
    
    # Prepare metadata list and documents list
    metadatas = [{"category": category, "text": text} for text in texts]
    documents = [text for text in texts]  # The original advice text as documents
    
    # Add data to the collection using 'documents' and 'metadatas' fields
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"Added {len(texts)} items to the '{category}' category in the vector store.")

def retrieve_context_by_category(query, category, top_k=3):
    # Encode the query into an embedding
    query_embedding = embedding_model.encode([query])[0]

    # Perform a search using 'query_embeddings' and apply category filtering
    results = collection.query(
        query_embeddings=[query_embedding],
        where={"category": category}
    )

    # Check if the query returned valid documents
    if not results.get("documents") or not results["documents"][0]:
        print("No relevant documents found for the query.")
        print("Raw query results:", results)
        return ["No specific advice available for this topic."]

    # Extract text content from documents, limited to top_k results
    return [doc for doc in results["documents"][0][:top_k]]
