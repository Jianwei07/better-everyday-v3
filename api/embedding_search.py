from sentence_transformers import SentenceTransformer
import chromadb
from api.config import EMBEDDING_MODEL_NAME, VECTOR_DB_NAME

# Initialize embedding model and vector database client
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
client = chromadb.Client()
collection = client.get_or_create_collection(VECTOR_DB_NAME)

def add_embeddings(texts, metadata):
    """Generate and store embeddings in the vector database."""
    embeddings = embedding_model.encode(texts)
    for i, embedding in enumerate(embeddings):
        collection.add(text_id=f"text_{i}", embedding=embedding, metadata=metadata[i])

def retrieve_similar_texts(query, top_k=3):
    """Retrieve similar texts based on the query embedding."""
    query_embedding = embedding_model.encode([query])[0]
    results = collection.query(embedding=query_embedding, top_k=top_k)
    return [result['metadata']['text'] for result in results]
