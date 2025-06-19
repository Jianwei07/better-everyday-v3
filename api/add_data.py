import argparse
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# Import the client directly from config, not the removed global 'collection'
from config import EMBEDDING_MODEL_NAME, CHROMA_PATH, client
import os
import shutil

# This will be used by LangChain's Chroma.from_documents
embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def load_documents(data_path):
    loader = DirectoryLoader(
        data_path,
        glob="*.md",
        loader_cls=lambda path: TextLoader(path, encoding="utf-8")
    )
    documents = loader.load()
    print(f"[INFO] Loaded {len(documents)} documents from {data_path}")
    return documents

def split_text(documents, chunk_size, chunk_overlap, category):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    for chunk in chunks:
        # Ensure category is lowercase and consistent for metadata
        chunk.metadata["category"] = category.strip().lower()
    print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap}) [category: {category}]")
    chunk_lengths = [len(c.page_content) for c in chunks]
    print(f"[STATS] Chunk sizes: min={min(chunk_lengths)}, max={max(chunk_lengths)}, avg={sum(chunk_lengths)//len(chunk_lengths)}")
    if chunks:
        print(f"[SAMPLE] Chunk content (first chunk): {chunks[0].page_content[:250]}...")
        print(f"[SAMPLE] Chunk metadata: {chunks[0].metadata}")
    print("\n[DEBUG] First 5 chunk metadatas for verification:")
    for i, chunk in enumerate(chunks[:5]):
        print(f"  Chunk {i}: {chunk.metadata}")
    return chunks

# Key change here: Pass the category as collection_name
def save_to_chroma(chunks, category, reset_db=False): # Added 'category' argument
    # Determine the collection name based on the category
    collection_name = category.strip().lower()
    
    # If reset_db, remove the ENTIRE chroma_storage path.
    # This assumes you want to clear all collections if reset_db is true.
    # If you only want to clear a specific collection, ChromaDB.delete_collection(name=collection_name)
    # would be used, but LangChain's Chroma wrapper doesn't directly expose that easily.
    # For simplicity, if `reset_db` is true, we wipe the whole thing.
    if reset_db:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print(f"[INFO] Deleted existing Chroma DB at {CHROMA_PATH}")
        else:
            print(f"[INFO] Chroma DB path {CHROMA_PATH} does not exist, creating new.")
        
        # Create a brand new Chroma DB with the specified collection
        db = Chroma.from_documents(
            chunks, 
            embedding_function, 
            persist_directory=CHROMA_PATH,
            collection_name=collection_name, # THIS IS THE CRITICAL ADDITION
            client=client # Pass the client directly
        )
        print(f"[INFO] Created new Chroma DB with {len(chunks)} chunks in collection '{collection_name}'.")
    else:
        # Load or create the specific collection
        try:
            # Use the existing client to get or create the specific collection
            # This is how you target a specific collection for addition
            db = Chroma(
                client=client, # Pass the client
                collection_name=collection_name, # THIS IS THE CRITICAL ADDITION
                embedding_function=embedding_function,
                persist_directory=CHROMA_PATH # Still needed for LangChain's Chroma object
            )
            print(f"[INFO] Loaded existing Chroma DB collection '{collection_name}'.")
            db.add_documents(chunks)
            print(f"[INFO] Added {len(chunks)} new chunks to collection '{collection_name}'.")
        except Exception as e:
            # If the collection doesn't exist when trying to load and not reset_db, create it
            print(f"[WARNING] Collection '{collection_name}' not found or error loading: {e}. Creating new one.")
            db = Chroma.from_documents(
                chunks, 
                embedding_function, 
                persist_directory=CHROMA_PATH,
                collection_name=collection_name, # THIS IS THE CRITICAL ADDITION
                client=client # Pass the client directly
            )
            print(f"[INFO] Created new Chroma DB with {len(chunks)} chunks in collection '{collection_name}'.")
            
def main():
    parser = argparse.ArgumentParser(description="Ingest data into topic-specific ChromaDB collections.")
    parser.add_argument("--chunk_size", type=int, default=300)
    parser.add_argument("--chunk_overlap", type=int, default=100)
    parser.add_argument("--data_path", type=str, default="data/neuro")
    parser.add_argument("--category", type=str, required=True, help="Category to tag and create/use collection for (e.g., neuro, fitness, optometry).")
    parser.add_argument("--reset_db", action="store_true", help="If set, deletes and recreates ALL ChromaDB data.")
    args = parser.parse_args()

    print(f"\n[RUNNING] Ingesting data from {args.data_path} with chunk_size={args.chunk_size}, chunk_overlap={args.chunk_overlap}, category={args.category}\n")
    documents = load_documents(args.data_path)
    chunks = split_text(documents, args.chunk_size, args.chunk_overlap, args.category)
    # Pass the category to save_to_chroma
    save_to_chroma(chunks, args.category, reset_db=args.reset_db) 

if __name__ == "__main__":
    main()